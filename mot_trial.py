from psychopy import core, event, visual
import random
from orbiting_circles import OrbitingCircles
import csv
from trial import Trial
from mot_response_handler import MOTResponseHandler

class MOTTrial(Trial):
    def __init__(self, win, trial_number, target_set_size, targets, targets_side, form, trial_type, layout, highlight_target):
        super().__init__(win, trial_number, target_set_size, targets, targets_side, form, trial_type, layout, highlight_target)
        self.objects = OrbitingCircles(win, self.target_set_size, self.targets, self.targets_side)
        self.response_handler = MOTResponseHandler(win)

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
        
        correct_response = self.highlighted_indices

        self.save_data(self.response_handler.clicked_object, correct_response, is_correct)

        t2 = core.getTime()

        print("Time:", t2 - t1)

        self.wait_for_input()
