from math import pi

participants_path = "data/participants"
fieldnames = ['UserID', 'First Name', 'Last Name', 'Age', 'Sex', 'Handedness', 'E-mail', 'Trial Number', 'Block number', 'Trial Type','Target Set Size', 'Target Side', "Layout", "Highlighted Target", "Response", "Correct Response", "Correctness", "TrialID", "ConditionID", "Images", "Targets"]
scale = 1080
target_color="blue"
mirror_color="yellow"
response_circle_radius = 0.1
response_circle_target_color = "green"
response_circle_mirror_color = "red"
feedback_color = "black"
feedback_font_size = 0.05

orbit_radius = 0.06
images_orbit_radius = 0.08
image_radius = 0.08
image_cover_radius = 0.05
image_highlight_radius = 0.07
orbiting_speed = 3/2 * pi # 3/2 * pi = 270 deg/s

cue_time = 1.5 # seconds
probe_time = 1.5 # seconds

mot_target_color = "blue"
mit_target_color = "magenta"

max_response_time_mot = 2.5  # seconds
max_response_time_mit = 5.0  # seconds

training_on = False
eyetracker_on = False