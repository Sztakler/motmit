from psychopy import core
from orbiting_images import OrbitingImages
from trial import Trial
from mit_response_handler import MITResponseHandler
from utils.input import wait_for_input

class Form():
    def __init__(self):
        pass

class MITTrial(Trial):
    def __init__(self, win, trial_number, block_number, target_set_size, targets, targets_side, form, trial_type, layout, highlight_target, filename, images_paths=None):
        super().__init__(win, trial_number, block_number, target_set_size, targets, targets_side, form, trial_type, layout, highlight_target, filename)
        self.objects = OrbitingImages(win, self.target_set_size, self.targets, self.targets_side, images_paths=images_paths)
        self.response_handler = MITResponseHandler(win, images_paths=images_paths)

    def draw_probe(self):
        delay = 0.5
        self.draw_fixation_cross()
        self.objects.draw_static(core.getTime())
        self.objects.cover()
        self.highlighted_indices = self.objects.highlight_object(self.highlight_target)
        self.win.flip()
        core.wait(delay)

    def handle_response(self):
        self.response_handler.get_response()
        is_correct = self.response_handler.check_correctness(self.highlight_target, self.targets, self.highlighted_indices, self.objects)
        self.response_handler.display_feedback()
        
        correct_response = self.objects.images_paths[self.highlighted_indices[0]]

        self.save_data(self.response_handler.clicked_object, correct_response, is_correct)
        wait_for_input(self.win)

        