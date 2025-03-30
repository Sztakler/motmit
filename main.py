from psychopy import core, visual, event
import random
import csv
from target import Target
from mot_trial import MOTTrial
from mit_trial import MITTrial

# Create a window
win = visual.Window([1920,1080], units="height", fullscr=True)


def get_mirror_orbit_index(orbit_index):
    return (orbit_index + orbits_on_side) % (2 * orbits_on_side) 

orbits_on_side = 3
combinations = []
for trial_type in ['mot', 'mit']:
    for highlight_target in [True, False]:
        for target_set_size in [2, 3]:
            for target_side in [0, 1]:
                orbit_indices = [[0, 1, 2], [0, 1, 2], [0, 1, 2]]
                if target_set_size == 2:
                    orbit_indices = [[0, 1], [1, 2], [0, 2]]
                orbit_indices = [[element + orbits_on_side * target_side for element in orbit_index] for orbit_index in orbit_indices]
                for indices in orbit_indices:
                    targets = []
                    for orbit_index in indices:
                        circle_index = random.choice([0, 1])
                        mirror_orbit_index = get_mirror_orbit_index(orbit_index)
                        targets.append(Target(orbit_index, mirror_orbit_index, circle_index))
                    combinations.append((target_set_size, targets, target_side, trial_type, highlight_target))

combinations *= 2
random.shuffle(combinations)
print(combinations[0])
print(len(combinations))

images_directory = "images"
image_count = 28
images_paths = [f"{images_directory}/{i}.png" for i in range(1, image_count + 1)]

selected_combinations = combinations[:]

form = None

for trial_number, (target_set_size, targets, target_side, trial_type, highlight_target) in enumerate(selected_combinations, start=1):
    trial = None
    if trial_type == "mot":
        trial = MOTTrial(win, trial_number, target_set_size, targets, target_side, form, trial_type, highlight_target)
    else:
        trial = MITTrial(win, trial_number, target_set_size, targets, target_side, form, trial_type, highlight_target, images_paths)
    trial.run()