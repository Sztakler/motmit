import math
from psychopy import visual, event, core
from response_handler import ResponseHandler
from config import scale, mit_target_color, image_radius, max_response_time_mit

class MITResponseHandler(ResponseHandler):
    def __init__(self, win):
        super().__init__(win)
        self.carousel_radius = 350 * scale
        self.items = [] # List of ImageStim objects in the carousel

    def construct_carousel(self, all_objects_data):
        """
        Creates a circular gallery of all images used in the current trial.
        """
        # Clear items list before constructing the new carousel
        self.items = []
        # Collect all unique image paths from the trial's object pairs
        image_paths = []
        for obj in all_objects_data:
            image_paths.extend(obj.image_pair)

        # Remove duplicates
        image_paths = list(set(image_paths))
        
        # Sort paths to maintain consistent gallery order
        image_paths.sort()
        
        # Add the '0a.png' distractor icon to the list
        image_paths.insert(0, "images/0a.png")
        
        # Calculate positions on a circle
        count = len(image_paths)
        positions = [
            (self.carousel_radius * math.cos(2 * math.pi * i / count + math.pi / 2),
             self.carousel_radius * math.sin(2 * math.pi * i / count + math.pi / 2))
            for i in range(count)
        ]

        # Create ImageStim objects
        for path, pos in zip(image_paths, positions):
            stim = visual.ImageStim(
                self.win, image=path, pos=pos, 
                size=(image_radius * 1.2) * scale # Slightly larger for better visibility
            )
            self.items.append(stim)

    def get_response(self, all_objects_data):
        """
        Displays the carousel and waits for a selection.
        """
        self.construct_carousel(all_objects_data)
        mouse = event.Mouse(win=self.win)
        mouse.setPos((0, 0))
        timer = core.Clock()
        self.win.flip()
        start_time = core.getTime()
        timeout = max_response_time_mit

        while timer.getTime() < timeout and not self.clicked_object:
            # Draw all elements of the carousel
            for item in self.items:
                item.draw()
                
            # Check for clicked elements
            if any(mouse.getPressed()):
                for item in self.items:
                    if mouse.isPressedIn(item):
                        # Calculate response time (current time - start time)
                        self.response_time = core.getTime() - start_time;
                        # Visual feedback for selection
                        highlight = visual.Circle(
                            self.win, radius=(image_radius * 0.7) * scale, 
                            fillColor=None, lineColor=mit_target_color, lineWidth=5, pos=item.pos
                        )
                        item.draw()
                        highlight.draw()
                        self.win.flip()
                    
                        self.clicked_object = item.image # This is the file path
                        core.wait(0.3)
                        break
            self.win.flip()

    def check_correctness(self, probe_image_path, is_target_probed):
        """
        Checks if the clicked image matches the identity of the probed object.
        """
        if is_target_probed:
            # Must match the exact image path of the probed target
            self.correct = (self.clicked_object == probe_image_path)
        else:
            # If a distractor was probed, the participant must click the '0a.png' icon
            self.correct = (self.clicked_object == "images/0a.png")
            
        self.feedback = "Dobrze." if self.correct else "Źle."
        return self.correct
