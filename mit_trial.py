from psychopy import core, event, visual
import random
from orbiting_images import OrbitingImages
import csv
from trial import Trial
from mit_response_handler import MITResponseHandler

class Form():
    def __init__(self):
        pass

class MITTrial(Trial):
    def __init__(self, win, trial_number, target_set_size, targets, targets_side, form, trial_type, highlight_target, images_paths=None):
        super().__init__(win, trial_number, target_set_size, targets, targets_side, form, trial_type, highlight_target)
        self.objects = OrbitingImages(win, self.target_set_size, self.targets, self.targets_side, images_paths=images_paths)
        self.response_handler = MITResponseHandler(win, images_paths=images_paths)

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
        self.objects.cover()
        self.highlighted_indices = self.objects.highlight_object(self.highlight_target)
        self.win.flip()
        core.wait(delay)

    def run(self):
        t1 = core.getTime()
        self.draw_fixation_cross()
        self.draw_cue()
        self.draw_tracking()
        self.draw_stop()
        self.draw_probe()

        self.response_handler.get_response()
        is_correct = self.response_handler.check_correctness(self.highlight_target, self.targets, self.objects)
        self.response_handler.display_feedback()
        
        self.save_data(self.response_handler.clicked_item, is_correct)

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