from psychopy import core, event, visual
from response_handler import ResponseHandler
from config import scale, response_circle_radius, response_circle_target_color, response_circle_mirror_color, max_response_time_mot

class MOTResponseHandler(ResponseHandler):
    def __init__(self, win):
        """
        Initialize the ResponseHandler instance.
        """
        super().__init__(win)
        self.green_circle = visual.Circle(self.win, radius=response_circle_radius * scale, fillColor=response_circle_target_color, pos=(-0.2 * scale, 0))
        self.red_circle = visual.Circle(self.win, radius=response_circle_radius * scale, fillColor=response_circle_mirror_color, pos=(0.2 * scale, 0))

    def get_response(self):
        self.green_circle.draw()
        self.red_circle.draw()
        self.win.flip()
        mouse = event.Mouse(win=self.win)

        timer = core.Clock()
        mouse.setPos((0, 0))  # Reset mouse position
        while not self.clicked_object and timer.getTime() < max_response_time_mot:
            if mouse.isPressedIn(self.green_circle):
                self.clicked_object = response_circle_target_color
            elif mouse.isPressedIn(self.red_circle):
                self.clicked_object = response_circle_mirror_color
    
    def check_correctness(self, is_target_highlighted):
        """
        Check the correctness of the response.

        Returns:
            bool: True if the response is correct, False otherwise.
        """
        # Checking the correctness of the response
        if self.clicked_object == response_circle_target_color:
            if is_target_highlighted:
                self.feedback = "Dobrze."
                self.correct = True
            else:
                self.feedback = "Źle."
                self.correct = False
        elif self.clicked_object == response_circle_mirror_color:
            if not is_target_highlighted:
                self.feedback = "Dobrze."
                self.correct = True
            else:
                self.feedback = "Źle."
                self.correct = False
        
        return self.correct

    def check_correctness_training(self, is_target_highlighted):
        """
        Check the correctness of the response. And provide verbose feedback.

        Returns:
            bool: True if the response is correct, False otherwise.
        """
        # Checking the correctness of the response
        if self.clicked_object == response_circle_target_color:
            if is_target_highlighted:
                self.feedback = "Dobrze."
                self.correct = True
            else:
                self.feedback = "Źle."
                self.correct = False
        elif self.clicked_object == response_circle_mirror_color:
            if not is_target_highlighted:
                self.feedback = "Dobrze."
                self.correct = True
            else:
                self.feedback = "Źle."
                self.correct = False
        return self.correct
