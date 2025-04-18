from psychopy import core, visual

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

    def display_feedback(self):
        feedback_duration = 1.5 
        feedback_message = visual.TextStim(self.win, text=self.feedback, color='black', height=0.05)
        continue_prompt = visual.TextStim(self.win, text="Naciśnij 'escape', by zakończyć badanie. Naciśnij dowolny przycisk, by kontynuować.", color='black', height=0.05, pos=(0, -0.2))
        feedback_message.draw()
        continue_prompt.draw()
        self.win.flip()
        core.wait(feedback_duration)
