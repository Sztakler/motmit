from psychopy import core, visual, event
import random
import csv
from fixation_cross import FixationCross
import uuid
from config import filename

class Form():
    def __init__(self):
        pass

class Trial:
    def __init__(self, win, trial_number, target_set_size, targets, targets_side, form, trial_type, layout, highlight_target):
        self.win = win
        self.trial_number = trial_number
        self.orbit_radius = 0.1
        self.speed = 0.5
        self.target_set_size = target_set_size
        self.targets = targets
        self.targets_side = targets_side
        self.form = form
        self.trial_type = trial_type
        self.cross = FixationCross(win, size=0.05)
        self.interrupted = False
        self.highlight_target = highlight_target
        self.response_handler = None
        self.highlighted_indices = None
        self.layout = layout
        self.id = uuid.uuid4()
      
    def split_time(self, time, n):
        cuts = sorted([random.uniform(0, time) for _ in range(n - 1)])
        intervals = [cuts[0]] + [cuts[i] - cuts[i-1] for i in range(1, n-1)] + [time - cuts[-1]]
        return intervals

    def draw_fixation_cross(self):
        self.cross.draw()

    def draw_fixation(self):
        self.draw_fixation_cross()
        self.win.flip()
        core.wait(0.5)

    def draw_cue(self):
        delay = 0.75
        start_time = core.getTime()
        self.objects.draw_static(start_time)
        self.objects.highlight_target()
        self.win.flip()
        core.wait(delay)

    def draw_stop(self):
        delay = 0.5
        self.objects.draw_static(core.getTime())
        self.draw_fixation_cross()
        self.win.flip()
        core.wait(delay)

    def draw_probe(self):
        delay = 0.5
        self.draw_fixation_cross()
        self.objects.draw_static(core.getTime())
        self.highlighted_indices = self.objects.highlight_object(self.highlight_target)
        self.win.flip()
        core.wait(delay)

    def draw_tracking(self):
        initial_direction_movement_time = 1.0
        change_direction_time = 0.75
        new_direction_movement_time = 0.75

        start_time = core.getTime()
        while core.getTime() - start_time < initial_direction_movement_time:
            self.objects.animate(start_time)
            self.draw_fixation_cross()      
            self.win.flip()
            if 'escape' in event.getKeys():
                core.quit()

        current_time = core.getTime() - start_time
        self.objects.update_initial_angles(current_time)
        intervals = self.split_time(change_direction_time, self.objects.number_of_pairs)
        indexes = list(range(self.objects.number_of_pairs))
        random.shuffle(indexes)
        clock = core.Clock()
        for interval, index in zip(intervals, indexes):
            start_time = core.getTime()
            clock.reset()
            while clock.getTime() < interval:
                self.objects.animate(start_time)
                self.draw_fixation_cross()      
                self.win.flip()
                if 'escape' in event.getKeys():
                    core.quit()
            current_time = core.getTime() - start_time
            self.objects.update_initial_angles(current_time)
            self.objects.orbits[index].change_direction()
        
        start_time = core.getTime()
        while core.getTime() - start_time < new_direction_movement_time:
            self.objects.animate(start_time)
            self.draw_fixation_cross()     
            self.win.flip()
            if 'escape' in event.getKeys():
                core.quit()

    def run(self):
        t1 = core.getTime()
        self.draw_fixation_cross()
        self.draw_cue()
        self.draw_tracking()
        self.draw_stop()
        self.draw_probe()

        self.response_handler.get_response()
        is_correct = self.response_handler.check_correctness(self.highlight_target)
        self.response_handler.display_feedback()
        
        self.save_data(self.response_handler.clicked_object, is_correct)
    
        t2 = core.getTime()

        print("Time:", t2 - t1)

        self.wait_for_input()

    def wait_for_input(self):   
        while True:
            keys = event.getKeys()
            if 'escape' in keys:
                core.quit()
            if keys:
                break

    def save_data(self, response, correct_response, correctness):
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            condition_id = self.generate_condition_id()
            #                'ID',         'First Name',         'Last Name',         'Age',         'Sex',         'Handedness',         'E-mail',        'Trial Number',    'Trial Type',     'Target Set Size',  'Target Side',      "Layout",       "Probing",         "Response", "Correct Response", "Correctness", "TrialID", "ConditionID"])
            writer.writerow([self.form.id, self.form.first_name, self.form.last_name, self.form.age, self.form.sex, self.form.handedness, self.form.email, self.trial_number, self.trial_type, self.target_set_size, self.targets_side, self.layout, self.highlight_target, response, correct_response, correctness, self.id, condition_id])

    def generate_condition_id(self):
        """
        Generates a unique condition ID based on the attributes of the object.
        The method encodes various attributes into a binary string representation
        to uniquely identify a condition. The encoding is based on predefined mappings
        for trial type, target side, probing, set size, and layout.
        Returns:
            str: A string representing the condition ID, or an error message
                 if any input is invalid.
        Attributes:
            self.trial_type (str): The type of trial, expected values are "mot" or "mit".
            self.targets_side (str): The side of the targets, expected values are "l" (left) or "r" (right).
            self.target_set_size (str): The size of the target set, expected values are "2" or "3".
            self.highlight_target (bool): Whether the target or distractor is highlighted, expected values are True or False.
            self.layout (list): The layout configuration, expected values are [0, 1, 2], [0, 1], [1, 2], or [0, 2].
        Encoding:
            - trial_type_map: {"mot": "0", "mit": "1"}
            - target_side_map: {"l": "0", "r": "1"}
            - probing_map: {False: "0", True: "1"}
            - set_size_map: {"2": "0", "3": "1"}
            - layout_map:
                [0, 1, 2] -> "0"
                [0, 1] -> "1"
                [1, 2] -> "2"
                [0, 2] -> "3"
        Example:
            ("mit", "r", "3", False, [1, 2]) -> Output: 11102
        Notes:
            If any of the attributes have an invalid value, the method returns
            "Error: Invalid input".
        """
        trial_type_map = {"mot": "0", "mit": "1"}
        target_side_map = {0: "0", 1: "1"}
        probing_map = {False: "0", True: "1"}
        set_size_map = {2: "0", 3: "1"}

        # Encode layout
        if self.layout == [0, 1, 2]:
            layout_encoded = "0"
        elif self.layout == [0, 1]:
            layout_encoded = "1"
        elif self.layout == [1, 2]:
            layout_encoded = "2"
        elif self.layout == [0, 2]:
            layout_encoded = "3"
        else:
            layout_encoded = "Invalid"

        # Encode each condition
        trial_type_encoded = trial_type_map.get(self.trial_type, "Invalid")
        target_side_encoded = target_side_map.get(self.targets_side, "Invalid")
        set_size_encoded = set_size_map.get(self.target_set_size, "Invalid")
        probing_encoded = probing_map.get(self.highlight_target, "Invalid")

        print("ENCODED", trial_type_encoded, target_side_encoded, set_size_encoded, probing_encoded, layout_encoded)

        # Check for invalid inputs
        if "Invalid" in (trial_type_encoded, target_side_encoded, set_size_encoded, layout_encoded):
            return "Error: Invalid input"

        # Combine the binary encoding
        return trial_type_encoded + target_side_encoded + set_size_encoded + probing_encoded + layout_encoded

class FixationCross:
    def __init__(self, win, size):
        self.lines = [
            visual.Line(win, start=(-size, 0), end=(size, 0), lineColor='black', lineWidth=2),
            visual.Line(win, start=(0, -size), end=(0, size), lineColor='black', lineWidth=2)
        ]
    
    def draw(self):
        for line in self.lines:
            line.draw()