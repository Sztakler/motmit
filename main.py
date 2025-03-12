from psychopy import core, visual, event
from trial import Trial
from participant_form import ParticipantForm
import random
import csv
from target import Target

"""
Połowa triali - target
połowa - dystraktor

Gdy śnieżynki sie zatrzymują podświatlamy target albo dystraktor. W MIT odpowiedz dwuetapowa. Czerwone i zielone kółko -- target czy 
dystraktor. Potem w kręgu śnieżynki i pytanie, która była podświetlona. W MOT odpowiedz jednoetapowa. W MIT wyświetlamy kółko z 6
śnieżynkami i jeśli target to wybiera właściwą śnieżynkę, a jeśli dystraktor to X (na godzinie dwunastej). Setsize mówi ile jest
targetów. Zawsze jest 12 obiektów na ekranie. Po 6 w kolumnie, 2 w orbicie.

W MIT i MOT się klika w odpowiedzi. Nie ma odpowiedzi tekstowych.

Jeśli badany ruszył oczami albo eeg się zepsuło, to próba jest wywalana i zapisywana w liście prób przerwanych. Trzeba tam zapisać 
wszystkie informacje o próbie. To się chyba nazywa repetition list.
Gdy badany skończył próby podstawowe to rusza repetition list (w randomowej kolejności). Powtarza 50% bloku podstawowego.
"""


win = visual.Window([600, 600])  # Zmieniono rozmiar okna na kwadratowy

# Pobranie danych badanego za pomocą formularza
form = ParticipantForm(win)
# form.show_form()

orbits_on_side = 3

def get_mirror_orbit_index(orbit_index):
    return (orbit_index + orbits_on_side) % (2 * orbits_on_side) 

# Utworzenie pliku CSV z nagłówkami
with open('experiment_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Trial Number", "Trial type", "Set Size", "Orbit Index", "Response", "Correct", "Email", "Gender", "First Name", "Last Name"])


combinations = []
for trial_type in [ 'mot']:
    for target_set_size in [2, 3]:
        for target_side in [0, 1]:
            orbit_indices = [[0, 1, 2]]
            if target_set_size == 2:
                orbit_indices = [[0, 1], [1, 2], [0, 2]]
            orbit_indices = [[element + orbits_on_side * target_side for element in orbit_index] for orbit_index in orbit_indices]
            for indices in orbit_indices:
                targets = []
                for orbit_index in indices:
                    circle_index = random.choice([0, 1])
                    mirror_orbit_index = get_mirror_orbit_index(orbit_index)
                    targets.append(Target(orbit_index, mirror_orbit_index, circle_index))
                combinations.append((target_set_size, targets, target_side, trial_type))

print("combinations: ", len(combinations))

# Wydłużenie listy kombinacji
combinations *= 3

# Pomieszanie kombinacji
random.shuffle(combinations)

# Wybór losowych kombinacji dla triali. Można podać jako argument [:n] by wybrać n pierwszych kombinacji
selected_combinations = combinations[:]

images_directory = "snowflakes"
image_count = 28
images_paths = [f"{images_directory}/{i}.png" for i in range(1, image_count + 1)]

repetition_list = []

for trial_number, (target_set_size, targets, target_side, trial_type) in enumerate(selected_combinations, start=1):
    trial = Trial(win, trial_number, target_set_size, targets, target_side, form, trial_type, images_paths)
    trial.run()
    if trial.interrupted:
        repetition_list.append(trial)

for trial in repetition_list:
    print(trial.trial_number, trial.target_set_size, trial.orbit_index, trial.direction, trial.target_side, trial.trial_type)
    trial.run()

win.close()
core.quit()
