from psychopy import core, visual, event
import random
import csv
from fixation_cross import FixationCross
import uuid
from config import scale, mot_target_color, mit_target_color
from eyetracker import eyetracker
from logger import logger
from utils.input import wait_for_input

class Trial:
    def __init__(self, win, trial_number, block_number, target_set_size, targets, targets_side, form, trial_type, layout, highlight_target, filename, feedback_color):
        self.win = win
        self.trial_number = trial_number
        self.block_number = block_number
        self.orbit_radius = 0.1 * scale
        self.speed = 0.5
        self.target_set_size = target_set_size
        self.targets = targets
        self.targets_side = targets_side
        self.form = form
        self.trial_type = trial_type
        self.cross = FixationCross(win, size=0.05 * scale)
        self.interrupted = False
        self.highlight_target = highlight_target
        self.response_handler = None
        self.highlighted_indices = None
        self.layout = layout
        self.id = uuid.uuid4()
        self.filename = filename
        self.feedback_color = feedback_color
      
    def reset(self):
        self.interrupted = False
        self.highlighted_indices = None
        self.response_handler.clicked_object = None
        self.response_handler.feedback = None
        self.response_handler.correct = None

    def split_time(self, time, n):
        cuts = sorted([random.uniform(0, time) for _ in range(n - 1)])
        intervals = [cuts[0]] + [cuts[i] - cuts[i-1] for i in range(1, n-1)] + [time - cuts[-1]]
        return intervals

    def draw_fixation_cross(self):
        self.cross.draw()

    def draw_fixation(self):
        delay = 0.75
        clock = core.Clock()
        clock.reset()
        
        color = "niebieskie"
        if self.feedback_color ==  mit_target_color:
            color = "różowe"

        while clock.getTime() < delay:
            message = visual.TextStim(self.win, text=f"Proszę śledzić {color} obiekty", color=self.feedback_color, height=0.05 * scale, pos=(0.0, 0.0 * scale))
            message.draw()
            self.win.flip()
            core.wait(0.01)

        while clock.getTime() < delay:
            eye_contact = eyetracker.check_position() and eyetracker.check_blink()
            self.draw_fixation_cross()
            self.win.flip()
            core.wait(0.01)

            # if not eye_contact:
            #     return False
            
        return True

    def draw_cue(self):
        delay = 1.0
        start_time = core.getTime()
        while core.getTime() - start_time < delay:
            eye_contact = eyetracker.check_position() and eyetracker.check_blink()

            self.draw_fixation_cross()
            self.objects.draw_static(start_time)
            self.objects.highlight_target()
            self.win.flip()

            if not eye_contact:
                return False
            
        return True

    def draw_stop(self):
        delay = 0.5
        start_time = core.getTime()
        while core.getTime() - start_time < delay:
            self.objects.draw_static(start_time)
            self.draw_fixation_cross()
            self.win.flip()


    def draw_probe(self):
        delay = 1.0
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
            eye_contact = eyetracker.check_position() and eyetracker.check_blink()
            
            self.objects.animate(start_time)
            self.draw_fixation_cross()      
            self.win.flip()
            if 'escape' in event.getKeys():
                core.quit()
            
            if not eye_contact:
                return False

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
                eye_contact = eyetracker.check_position() and eyetracker.check_blink()

                self.objects.animate(start_time)
                self.draw_fixation_cross()      
                self.win.flip()
                if 'escape' in event.getKeys():
                    core.quit()
                
                # if not eye_contact:
                #     return False
                
            current_time = core.getTime() - start_time
            self.objects.update_initial_angles(current_time)
            self.objects.orbits[index].change_direction()
        
        start_time = core.getTime()
        while core.getTime() - start_time < new_direction_movement_time:
            eye_contact = eyetracker.check_position() and eyetracker.check_blink()
            
            self.objects.animate(start_time)
            self.draw_fixation_cross()     
            self.win.flip()

            if 'escape' in event.getKeys():
                core.quit()
        
            if not eye_contact:
                return False
            
        return True

    def run_trial(self):
        logger.info("Start trial")

        self.win.mouseVisible = False

        if not self.draw_fixation(): 
            self.interrupted = True
            logger.warning("Lost eye contact in draw_fixation()")
            self.display_look_at_center_message_and_quit()
            return
        if not self.draw_cue(): 
            self.interrupted = True
            logger.warning("Lost eye contact in draw_cue()")
            self.display_look_at_center_message_and_quit()
            return
        if not self.draw_tracking(): 
            self.interrupted = True
            logger.warning("Lost eye contact in draw_tracking()")
            self.display_look_at_center_message_and_quit()
            return
        
        self.draw_stop()
        self.draw_probe()

        self.win.mouseVisible = True

    def handle_response(self, practiceMode=False):
        self.response_handler.get_response()
        is_correct = self.response_handler.check_correctness(self.highlight_target)
        self.response_handler.display_feedback(self.feedback_color)
        
        if not practiceMode:
            self.save_data(self.response_handler.clicked_object, is_correct)
        wait_for_input(self.win)

    def run(self, practiceMode=False):
        self.run_trial()
        if self.interrupted:
            return self.interrupted
        self.handle_response(practiceMode)
        return self.interrupted

    def display_look_at_center_message_and_quit(self):
        """Wyświetla komunikat o patrzeniu na środek i kończy trial."""
        message = visual.TextStim(self.win, text="Proszę patrzeć na środek i nie mrugać!", color='black', height=0.05 * scale, pos=(0, 0.15 * scale))
        clock = core.Clock()
        duration = 2.0  # ile sekund wyświetlamy komunikat
        
        clock.reset()
        while clock.getTime() < duration:
            self.draw_fixation_cross()
            message.draw()
            self.win.flip()
            if 'escape' in event.getKeys():
                core.quit()
        
        self.interrupted = True

    def save_data(self, response, correct_response, correctness):
        with open(self.filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            condition_id = self.generate_condition_id()
            #                'ID',         'First Name',         'Last Name',         'Age',         'Sex',         'Handedness',         'E-mail',        'Trial Number',    'Block Number'   'Trial Type',     'Target Set Size',  'Target Side',      "Layout",       "Probing",         "Response", "Correct Response", "Correctness", "TrialID", "ConditionID"])
            writer.writerow([self.form.id, self.form.first_name, self.form.last_name, self.form.age, self.form.sex, self.form.handedness, self.form.email, self.trial_number, self.block_number, self.trial_type, self.target_set_size, self.targets_side, self.layout, self.highlight_target, response, correct_response, correctness, self.id, condition_id])

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

        # print("ENCODED", trial_type_encoded, target_side_encoded, set_size_encoded, probing_encoded, layout_encoded)

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