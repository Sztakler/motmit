from math import pi

experiment_name = "MOT_MIT_EEG"
participants_path = "data/participants"
fieldnames = ['UserID', 'Age', 'Sex', 'Handedness', 'Trial Number', 'Block number', 'Trial Type','Target Set Size', 'Target Side', "Layout", "Highlighted Target", "Response", "Response Time", "Status", "Correct Response", "Correctness", "TrialID", "ConditionID", "Images", "Targets", "Clicked_Orbit_ID", "Clicked_Item_Idx", "Probe_Orbit_ID", "Probe_Item_Idx"]
scale = 1
target_color="blue"
mirror_color="yellow"
response_circle_radius = 108
response_circle_target_color = "green"
response_circle_mirror_color = "red"
feedback_color = "black"
feedback_font_size = 54

orbit_radius = 64.8
images_orbit_radius = 86.4
image_radius = 86.4
image_cover_radius = 54
image_highlight_radius = 75.6
orbiting_speed = 3/2 * pi # 3/2 * pi = 270 deg/s

cue_time = 1.5 # seconds
probe_time = 1.5 # seconds

mot_target_color = "blue"
mit_target_color = "magenta"

max_response_time_mot = 2.5  # seconds
max_response_time_mit = 5.0  # seconds

n_blocks = 4
n_selected_combinations = None

lpt_address = 0x3efc # standard LPT1 addres (hex)

training_on = True
eyetracker_on = True
form_on = True

