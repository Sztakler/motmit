from psychopy import visual, event, core
from response_handler import ResponseHandler
from config import scale, response_circle_radius, response_circle_target_color, response_circle_mirror_color, max_response_time_mot

class MOTResponseHandler(ResponseHandler):
    def __init__(self, win):
        super().__init__(win)
        # Position two choice circles on the screen
        self.target_circle = visual.Circle(
            self.win, radius=response_circle_radius * scale, 
            fillColor=response_circle_target_color, pos=(-200 * scale, 0)
        )
        self.distractor_circle = visual.Circle(
            self.win, radius=response_circle_radius * scale, 
            fillColor=response_circle_mirror_color, pos=(200 * scale, 0)
        )

    def get_response(self):
        """
        Waits for a mouse click on one of the two circles.
        """
        mouse = event.Mouse(win=self.win)
        mouse.setPos((0, 0))
        timer = core.Clock()
        timeout = max_response_time_mot

        # Draw and immediately start timer
        self.target_circle.draw()
        self.distractor_circle.draw()
        self.win.flip()
        start_time = core.getTime()
        
        while timer.getTime() < timeout:
            self.target_circle.draw()
            self.distractor_circle.draw()
            self.win.flip()

            if mouse.getPressed()[0]:
                if mouse.isPressedIn(self.target_circle):
                    self.clicked_object = "target"
                    self.response_time = core.getTime() - start_time
                    break
                elif mouse.isPressedIn(self.distractor_circle):
                    self.clicked_object = "distractor"
                    self.response_time = core.getTime() - start_time
                    break
        
    def check_correctness(self, is_target_probed):
        """
        Validates if the participant clicked the circle corresponding to the probe type.
        """
        if self.clicked_object == "target":
            self.correct = is_target_probed
        elif self.clicked_object == "distractor":
            self.correct = not is_target_probed
            
        self.feedback = "Dobrze." if self.correct else "Źle."
        return self.correct
