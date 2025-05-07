from math import pi

participants_path = "data/participants"
fieldnames = ['UserID', 'First Name', 'Last Name', 'Age', 'Sex', 'Handedness', 'E-mail', 'Trial Number', 'Trial Type','Target Set Size', 'Target Side', "Layout", "Probing", "Response", "Correct Response", "Correctness", "TrialID", "ConditionID"]
scale = 1080
target_color="blue"
mirror_color="yellow"
response_circle_radius = 0.1
response_circle_target_color = "green"
response_circle_mirror_color = "red"
feedback_color = "black"
feedback_font_size = 0.05

orbit_radius = 0.04
orbiting_speed = 3/2 * pi # 3/2 * pi = 270 deg/s