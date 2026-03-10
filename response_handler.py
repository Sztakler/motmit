from psychopy import visual, core
from config import scale, feedback_font_size

class ResponseHandler:
    """
    Base class for handling participant responses and feedback.
    """
    def __init__(self, win):
        self.win = win
        self.clicked_object = None
        self.feedback = "Brak odpowiedzi."
        self.correct = False
        self.response_time = -1 # Default value if no response

    def display_feedback(self):
        """
        Displays the result of the trial (Correct/Incorrect) to the participant.
        """
        # Create feedback text
        feedback_message = visual.TextStim(
            self.win, text=self.feedback, color="black", 
            height=feedback_font_size
        )
        # Create instruction to continue
        continue_prompt = visual.TextStim(
            self.win, text="Click any mouse button to continue.", 
            color="black", height=(feedback_font_size * 0.6) * scale, 
            pos=(0, -300 * scale)
        )
        
        feedback_message.draw()
        continue_prompt.draw()
        self.win.flip()

