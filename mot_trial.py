from psychopy import core, event, visual
import random
from orbiting_circles import OrbitingCircles
import csv
from trial import Trial
from mot_response_handler import MOTResponseHandler

class MOTTrial(Trial):
    def __init__(self, win, trial_number, target_set_size, targets, targets_side, form, trial_type, highlight_target):
        super().__init__(win, trial_number, target_set_size, targets, targets_side, form, trial_type, highlight_target)
        self.objects = OrbitingCircles(win, self.target_set_size, self.targets, self.targets_side)
        self.response_handler = MOTResponseHandler(win)