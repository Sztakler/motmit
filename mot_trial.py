from orbiting_images import OrbitingImages
from trial import Trial
from mot_response_handler import MOTResponseHandler
from utils.input import wait_for_input
from config import mot_target_color

class MOTTrial(Trial):
    def __init__(self, win, trial_number, block_number, target_set_size, targets, targets_side, form, trial_type, layout, highlight_target, filename, images_paths=None):
        print(images_paths)
        super().__init__(win, trial_number, block_number, target_set_size, targets, targets_side, form, trial_type, layout, highlight_target, filename)
        self.objects = OrbitingImages(win, self.target_set_size, self.targets, self.targets_side, images_paths=images_paths, target_color=mot_target_color)
        self.response_handler = MOTResponseHandler(win)

    def handle_response(self, practiceMode=False):
        self.response_handler.get_response()
        is_correct = self.response_handler.check_correctness(self.highlight_target)
        self.response_handler.display_feedback(mot_target_color)
        
        correct_response = self.highlighted_indices

        if not practiceMode:
            self.save_data(self.response_handler.clicked_object, correct_response, is_correct)
        wait_for_input(self.win)