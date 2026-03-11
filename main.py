from psychopy import visual, core, event
from experiment_view import ExperimentView
from scenarios_generator import generate_base_pool, get_full_experiment
from config import *
from response_manager import handle_response
from eyetracker import eyetracker
from data_manager import DataManager
from form import Form
import os
import re
from utils.input import wait_for_input

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

def display_feedback(win, message, color=feedback_color, await_input=True):
    """Displays short feedback message to the user."""
    feedback = visual.TextStim(win, text=message, color=color, height=feedback_font_size)
    feedback.draw()
    win.flip()
    if await_input:
        wait_for_input(win)

def display_look_at_center_message(win):
    """Wyświetla komunikat o patrzeniu na środek i kończy trial."""
    message = visual.TextStim(win, text="Proszę patrzeć na środek i nie mrugać. Naciśnij dowolny przycisk myszy, aby kontynuować.", color='black', height=feedback_font_size, pos=(0, 0))
    message.draw()
    win.flip()
    wait_for_input(win)


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

def run_trial(win, trial_config, is_practice=False):
    view = ExperimentView(win, trial_config, base_switch_time=TIME_MOVEMENT_START)
    fixation = FixationCross(win, size=54) # Assuming FixationCross is defined
    clock = core.Clock()

    # --- PHASE 0: Instruction Text ---
    color_name = "niebieskie" if trial_config.trial_type.name == "MOT" else "różowe"
    color_val = mot_target_color if trial_config.trial_type.name == "MOT" else mit_target_color
    
    # Hide mouse cursor
    win.mouseVisible = False
    
    display_feedback(win, message=f"Proszę śledzić {color_name} obiekty", 
                                color=color_val, await_input=False)
    core.wait(TIME_FIXATION_TEXT)
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
            display_look_at_center_message(win)
            return True, None
        
        view.update(t=0, show_targets=True)
        fixation.draw()
        win.flip()

    # --- PHASE 3: Tracking (Motion with direction change) ---
    clock.reset()
    while clock.getTime() < TIME_MOVEMENT_TOTAL:
        t = clock.getTime()

        if not (eyetracker.check_position() and eyetracker.check_blink()):
            display_look_at_center_message(win)
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

    # Show mouse cursor
    win.mouseVisible = True

    # --- PHASE 6: Response ---
    # win.mouseVisible = True
    # print(f"Correct answer: {trial_config.correct_answer}")
    # keys = event.waitKeys(keyList=['t', 'n', 'escape'])
    is_correct, response_val, response_time, c_orbit_id, c_item_idx = handle_response(win, trial_config, is_practice)
    print(f"Result: {is_correct}, Selected: {response_val}, Response Time: {response_time}")
    
    results = {
        'clicked_object': response_val,
        'correct_answer': trial_config.correct_answer, # should be different answer in MOT (target/distractor) and MIT (image path)
        'is_correct': is_correct,
        'response_time': response_time,
        'clicked_orbit_id': c_orbit_id,
        'clicked_item_idx': c_item_idx
    }

    if 'escape' in event.getKeys(): return True, results

    return False, results

if __name__ == "__main__":

    form = Form()
    if form_on:
        form.show_form()

    win = visual.Window([1920, 1080], fullscr=True, units='pix')
    images = get_images()
    base_pool = generate_base_pool()
    experiment_structure = get_full_experiment(base_pool, n_blocks)

    print(f"length: {len(experiment_structure[0])}")
    core.quit()

    eyetracker.config(win, experiment_name, form.id)
    
    csv_filename = f"data/participants/{form.id}_results.csv"
    data_saver = DataManager(csv_filename, form)

    # --- Practice Phase ---
    if training_on:
        practice_trials = experiment_structure[0]
        eyetracker.calibrate_and_start_recording()
        display_feedback(win, f"Zaczynasz blok testowy. Naciśnij dowolny przycisk myszy, aby rozpocząć.")

        for trial in practice_trials:
            eyetracker.start_recording()
            run_trial(win, trial, is_practice=training_on)
            eyetracker.stop_recording()

        display_feedback(win, "Koniec bloku testowego. Zrób sobie przerwę. Naciśnij dowolny przycisk myszy, aby przejść do badania.")


    interrupted_trials = []

    # --- Main Phase ---
    for b_idx, block in enumerate(experiment_structure, 1):
        # Calibrate eyetracker at the beginning of each block
        eyetracker.calibrate_and_start_recording()
        display_feedback(win, f"Zaczynasz blok {b_idx}. Naciśnij dowolny przycisk myszy, aby rozpocząć.")

        # Iterate through trials in the current block
        for trial in block:
            # Reset eyetracker state before each trial to flush data
            eyetracker.start_recording()
        
            interrupted, result = run_trial(win, trial)

            eyetracker.stop_recording()
            
            if interrupted:
                interrupted_trials.append(trial)
            else:
                data_saver.save_trial_data(trial, result)
                continue

            if 'escape' in event.getKeys():
                win.close()
                core.quit()
                

        # Handle break after each block except the last one
        if b_idx < n_blocks:
            display_feedback(win, "Koniec bloku. Zrób sobie przerwę. Naciśnij dowolny przycisk myszy, aby kontynuować.")

    
    # --- Interrupted Trials Phase ---
    if interrupted_trials:
        display_feedback(win, "Niektóre próby zostały przerwane. Naciśnij dowolny przycisk myszy, aby je powtórzyć.")
        eyetracker.calibrate_and_start_recording()
        display_feedback(win, "Zaczynasz blok powtórzeniowy. Naciśnij dowolny przycisk myszy, aby rozpocząć.")


        for trial in interrupted_trials[:len(interrupted_trials)//2]:
            # trial = interrupted_trials.pop(0)
            
            eyetracker.start_recording()
            interrupted, result = run_trial(win, trial)
            eyetracker.stop_recording()

            if interrupted:
                # interrupted_trials.append(trial)
                continue
            else:
                data_saver.save_trial_data(trial, result)
                continue

    display_feedback(win, "Koniec eksperymentu. Dziękujemy za udział.")

    win.close()
    core.quit()
            
