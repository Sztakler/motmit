from psychopy import core, visual, event
from config import scale, feedback_color, feedback_font_size

class ResponseHandler:
    """
    A class to handle responses for the application.
    """

    def __init__(self, win):
        """
        Initialize the ResponseHandler instance.
        """
        self.win = win
        self.response = None
        self.feedback = "Incorrect. No response provided."
        self.correct = None
        self.clicked_object = None

    def display_feedback(self, color=feedback_color):
        feedback_message = visual.TextStim(self.win, text=self.feedback, color=color, height=feedback_font_size * scale)
        continue_prompt = visual.TextStim(self.win, text="Naciśnij dowolny przycisk myszy, by kontynuować.", color=color, height=feedback_font_size * scale, pos=(0, -0.2 * self.win.size[1]))
        feedback_message.draw()
        continue_prompt.draw()
        self.win.flip()
