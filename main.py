from psychopy import visual, core, event
import random
import csv
from target import Target
from mot_trial import MOTTrial
from mit_trial import MITTrial
from form import Form
import os
from config import participants_path, fieldnames, feedback_color, feedback_font_size, scale, mit_target_color, mot_target_color, training_on, form_on, n_blocks, n_selected_combinations
from eyetracker import eyetracker
from utils.input import wait_for_input
from logger import logger

form = Form()

if form_on:
    form.show_form()
 
win = visual.Window([1920,1080], units="pix", fullscr=True)
    
def get_mirror_orbit_index(orbit_index):
    return (orbit_index + orbits_on_side) % (2 * orbits_on_side) 

def display_feedback(win, feedback_text):
    feedback = visual.TextStim(win, text=feedback_text, color=feedback_color, height=feedback_font_size * scale)
    feedback.draw()
    win.flip()
    wait_for_input(win)
    logger.info("Feedback displayed")

orbits_on_side = 3
combinations = []
for trial_type in ['mot', 'mit']:
    for highlight_target in [True, False]:
        for target_set_size in [2, 3]:
            for target_side in [0, 1]:
                layout_indices = [[0, 1, 2], [0, 1, 2], [0, 1, 2]]
                if target_set_size == 2:
                    layout_indices = [[0, 1], [1, 2], [0, 2]]
                orbit_indices = [[element + orbits_on_side * target_side for element in orbit_index] for orbit_index in layout_indices]
                for i, indices in enumerate(orbit_indices):
                    targets = []
                    for orbit_index in indices:
                        circle_index = random.choice([0, 1])
                        mirror_orbit_index = get_mirror_orbit_index(orbit_index)
                        targets.append(Target(orbit_index, mirror_orbit_index, circle_index))
                    layout = layout_indices[i]
                    combinations.append((target_set_size, targets, target_side, trial_type, highlight_target, layout))

combinations *= 2
random.shuffle(combinations)
                      
experimentName = "MOT_MIT"
images_directory = "images"
image_count = 11
images_paths =  [(f"{images_directory}/{i}a.png", f"{images_directory}/{i}b.png") for i in range(1, image_count + 1)]

selected_combinations = combinations[:n_selected_combinations]

# Create the data/participants catalogue if it doesn't exist
os.makedirs(participants_path, exist_ok=True)
filename = f"{participants_path}/{form.id}.csv"
file_exists = os.path.isfile(filename) and os.path.getsize(filename) > 0

eyetracker.config(win, experimentName, form.id)

with open(filename, mode="a", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    if not file_exists:
        writer.writeheader()

interrupted_trials = []

if training_on:
    logger.info(f"Practice block started")
    eyetracker.calibrate_and_start_recording()
    display_feedback(win, f"Zaczynasz blok testowy. Naciśnij dowolny przycisk myszy, aby rozpocząć.")

    for trial_number, (target_set_size, targets, target_side, trial_type, highlight_target, layout) in enumerate(selected_combinations[:len(selected_combinations) ], start=1):
        trial = None
        if trial_type == "mot":
            trial = MOTTrial(win, trial_number, 0, target_set_size, targets, target_side, form, trial_type, layout, highlight_target, filename, images_paths, mot_target_color)
        else:
            trial = MITTrial(win, trial_number, 0, target_set_size, targets, target_side, form, trial_type, layout, highlight_target, filename, images_paths, mit_target_color)
        
        eyetracker.start_recording()
        logger.info("Eyetracker started recording")
        interrupted = trial.run(practiceMode=True)
        win.flip()

    eyetracker.stop_recording()
    display_feedback(win, "Koniec bloku testowego. Zrób sobie przerwę. Naciśnij dowolny przycisk myszy, aby przejść do badania.")

for block in range(n_blocks):
    logger.info(f"Block {block + 1} started")
    eyetracker.calibrate_and_start_recording()
    random.shuffle(selected_combinations)
    display_feedback(win, f"Zaczynasz blok {block + 1}. Naciśnij dowolny przycisk myszy, aby rozpocząć.")

    for trial_number, (target_set_size, targets, target_side, trial_type, highlight_target, layout) in enumerate(selected_combinations, start=1):
        trial = None
        if trial_type == "mot":
            trial = MOTTrial(win, trial_number, block + 1, target_set_size, targets, target_side, form, trial_type, layout, highlight_target, filename, images_paths, mot_target_color)
        else:
            trial = MITTrial(win, trial_number, block + 1, target_set_size, targets, target_side, form, trial_type, layout, highlight_target, filename, images_paths, mit_target_color)
        
        eyetracker.start_recording()
        logger.info("Eyetracker started recording")
        interrupted = trial.run()
        win.flip()

    if interrupted:
        interrupted_trials.append(trial)

    eyetracker.stop_recording()
    if block != n_blocks - 1:
        display_feedback(win, "Koniec bloku. Zrób sobie przerwę. Naciśnij dowolny przycisk myszy, aby kontynuować.")

logger.info(f"Interrupted trials: {len(interrupted_trials)}")
if len(interrupted_trials) > 0:
        eyetracker.calibrate_and_start_recording()
        logger.info(f"Interrupted trials: {len(interrupted_trials)}")
        display_feedback(win, "Niektóre próby zostały przerwane. Naciśnij dowolny przycisk myszy, aby je powtórzyć.")
        for trial in interrupted_trials[:len(selected_combinations) // 2]:
            trial.reset()
            trial.run()
        interrupted_trials.clear()

display_feedback(win, "Koniec eksperymentu. Dziękujemy za udział.")

