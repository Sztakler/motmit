from psychopy import visual, core, event
from experiment_view import ExperimentView
from scenarios_generator import generate_base_pool, get_full_experiment
from config import *
from response_manager import handle_response
from eyetracker import eyetracker
from form import Form
import os
import re

class FixationCross:
    def __init__(self, win, size):
        self.lines = [
            visual.Line(win, start=(-size, 0), end=(size, 0), lineColor='black', lineWidth=2), # type: ignore
            visual.Line(win, start=(0, -size), end=(0, size), lineColor='black', lineWidth=2) # type: ignore
        ]
    
    def draw(self):
        for line in self.lines:
            line.draw()

def get_images(folder_path="images/"):
    """
    Scans the folder for files named like '0a.png', '0b.png', '10a.png', etc.
    Returns a sorted list of paths.
    """
    if not os.path.exists(folder_path):
        print(f"Warning: Folder '{folder_path}' not found.")
        return []

    # Regex breakdown:
    # ^\d+    -> Starts with one or more digits
    # [ab]    -> Followed by exactly 'a' or 'b'
    # \.png$  -> Ends with '.png'
    pattern = re.compile(r'^(\d+)[ab]\.png$')
    
    files = []
    for f in os.listdir(folder_path):
        match = pattern.match(f)
        if match:
            files.append(f)
    
    # Sort numerically based on the number part first, then the letter
    # This ensures: 0a, 0b, 1a, 1b ... 10a, 10b
    files.sort(key=lambda x: (int(pattern.match(x).group(1)), x)) # type: ignore
    
    return [os.path.join(folder_path, f) for f in files]

# --- PHASE DURATIONS (Based on your Trial class) ---
TIME_FIXATION_TEXT = 0.75  
TIME_FIXATION_CROSS = 0.5   
TIME_CUE = cue_time         
TIME_MOVEMENT_START = 1.0   
TIME_MOVEMENT_JITTER = 0.75 
TIME_MOVEMENT_END = 0.75    
TIME_STOP = 0.5             
TIME_PROBE = probe_time     

# Total movement duration for the loop
TIME_MOVEMENT_TOTAL = TIME_MOVEMENT_START + TIME_MOVEMENT_JITTER + TIME_MOVEMENT_END

def run_trial(win, trial_config):
    view = ExperimentView(win, trial_config, base_switch_time=TIME_MOVEMENT_START)
    fixation = FixationCross(win, size=20) # Assuming FixationCross is defined
    clock = core.Clock()

    # --- PHASE 0: Instruction Text ---
    color_name = mot_target_color if trial_config.trial_type.name == "MOT" else mit_target_color
    color_val = mot_target_color if trial_config.trial_type.name == "MOT" else mit_target_color
    instr_msg = visual.TextStim(win, text=f"Please track the {color_name} objects", 
                                color=color_val, height=30, units='pix')
    
    clock.reset()
    while clock.getTime() < TIME_FIXATION_TEXT:
        instr_msg.draw()
        win.flip()

    # --- PHASE 1: Fixation Cross ---
    clock.reset()
    while clock.getTime() < TIME_FIXATION_CROSS:
        fixation.draw()
        win.flip()

    # --- PHASE 2: Cue (Static targets highlighted) ---
    clock.reset()
    while clock.getTime() < TIME_CUE:
        if not (eyetracker.check_position() and eyetracker.check_blink()):
            return True, None
        
        view.update(t=0, show_targets=True)
        fixation.draw()
        win.flip()

    # --- PHASE 3: Tracking (Motion with direction change) ---
    clock.reset()
    while clock.getTime() < TIME_MOVEMENT_TOTAL:
        t = clock.getTime()

        if not (eyetracker.check_position() and eyetracker.check_blink()):
            return True, None
        
        view.update(t=t, show_targets=False)
        fixation.draw()
        win.flip()
        if 'escape' in event.getKeys(): core.quit()

    # --- PHASE 4: Stop (Static images before probe) ---
    clock.reset()
    while clock.getTime() < TIME_STOP:      
        view.update(t=TIME_MOVEMENT_TOTAL, show_targets=False)
        fixation.draw()
        win.flip()

    # --- PHASE 5: Probe (Highlight single object) ---
    clock.reset()
    while clock.getTime() < TIME_PROBE:
        view.update(t=TIME_MOVEMENT_TOTAL, probe_only=True)
        fixation.draw()
        win.flip()

    # --- PHASE 6: Response ---
    # win.mouseVisible = True
    # print(f"Correct answer: {trial_config.correct_answer}")
    # keys = event.waitKeys(keyList=['t', 'n', 'escape'])
    is_correct, response_val, response_time = handle_response(win, trial_config)
    print(f"Result: {is_correct}, Selected: {response_val}, Response Time: {response_time}")
    
    if 'escape' in event.getKeys(): return 'exit'

    return 'ok'

def run_break(win, current_block, total_blocks):
    """
    Displays a break screen between blocks.
    """
    message = f"Block {current_block} of {total_blocks} completed.\n\nTake a break!\nPress SPACE to continue."
    break_text = visual.TextStim(win, text=message, color='black', height=30)
    break_text.draw()
    win.flip()
    event.waitKeys(keyList=['space'])

if __name__ == "__main__":
    win = visual.Window([1920, 1080], fullscr=True, units='pix')
    images = get_images()
    base_pool = generate_base_pool()
    experiment_structure = get_full_experiment(base_pool, n_blocks)

    form = Form()
    if form_on:
        form.show_form()

    eyetracker.config(win, experiment_name, form.id)
    
    interrupted_trials = []

    for b_idx, block in enumerate(experiment_structure, 1):
        # Calibrate eyetracker at the beginning of each block
        eyetracker.calibrate_and_start_recording()

        # Iterate through trials in the current block
        for trial in block:
            # Reset eyetracker state before each trial to flush data
            eyetracker.start_recording()
        
            interrupted, result = run_trial(win, trial)
            
            if interrupted:
                interrupted_trials.append(trial)

            eyetracker.stop_recording()

            if result == 'exit':
                win.close()
                core.quit()
                
            # data_log.save_trial_data(trial, result_dict)

        # Handle break after each block except the last one
        if b_idx < n_blocks:
            run_break(win, b_idx, n_blocks)

    win.close()
    core.quit()
            
