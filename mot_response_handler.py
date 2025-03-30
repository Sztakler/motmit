from psychopy import core, event, visual

class MOTResponseHandler:
    def __init__(self, win):
        """
        Initialize the ResponseHandler instance.
        """
        self.win = win
        self.response = None
        self.feedback = "Incorrect. No response provided."
        self.correct = None
        self.clicked_circle = None
        self.green_circle = visual.Circle(self.win, radius=0.2, fillColor='green', pos=(-0.4, 0))
        self.red_circle = visual.Circle(self.win, radius=0.2, fillColor='red', pos=(0.4, 0))

    def get_response(self):
        self.green_circle.draw()
        self.red_circle.draw()
        self.win.flip()
        mouse = event.Mouse(win=self.win)

        timer = core.Clock()
        mouse.setPos((0, 0))  # Reset mouse position
        while not self.clicked_circle and timer.getTime() < 3:
            if mouse.isPressedIn(self.green_circle):
                self.clicked_circle = 'green'
            elif mouse.isPressedIn(self.red_circle):
                self.clicked_circle = 'red'
    
    def check_correctness(self, is_target_highlighted):
        """
        Check the correctness of the response.

        Returns:
            bool: True if the response is correct, False otherwise.
        """
        # Checking the correctness of the response
        if self.clicked_circle == 'green':
            if is_target_highlighted:
                self.feedback = "Poprawnie! Podświetlono cel."
                self.correct = True
            else:
                self.feedback = "Niepoprawnie. Podświetlono dystraktor."
                self.correct = False
        elif self.clicked_circle == 'red':
            if not is_target_highlighted:
                self.feedback = "Poprawnie! Podświetlono dystraktor."
                self.correct = True
            else:
                self.feedback = "Niepoprawnie. Podświetlono cel."
                self.correct = False
        
        return self.correct
    
    def display_feedback(self):
        feedback_duration = 1.5 
        feedback_message = visual.TextStim(self.win, text=self.feedback, color='black')
        feedback_message.draw()
        self.win.flip()
        core.wait(feedback_duration)
