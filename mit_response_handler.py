import math
from psychopy import visual, event, core
from response_handler import ResponseHandler
from config import scale, mit_target_color, image_radius, max_response_time_mit

class MITResponseHandler(ResponseHandler):
    def __init__(self, win):
        super().__init__(win)
        self.carousel_radius = 350 * scale
        self.items = [] # List of ImageStim objects in the carousel
        self.clicked_orbit_id = "N/A"
        self.clicked_item_idx = "N/A"

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

                        if item.image == "images/0a.png":
                            self.clicked_orbit_id = "distractor_icon"
                            self.clicked_item_idx = "distractor_icon"
                        else:
                            for orbit in all_objects_data:
                                # Simplified Orbit IDs to 0-2 (Top, Middle, Bottom) using modulo 3.
                                # Since the carousel displays unique images from both columns, we only track 
                                # the logical position. Side information is already stored in 'Target Side'.
                                if item.image == orbit.image_pair[orbit.target_idx]:
                                    self.clicked_orbit_id = orbit.orbit_id % 3
                                    self.clicked_item_idx = orbit.target_idx
                                    break
                                elif item.image == orbit.image_pair[orbit.distractor_idx]:
                                    self.clicked_orbit_id = orbit.orbit_id % 3
                                    self.clicked_item_idx = orbit.distractor_idx
                                    break
                        
                        core.wait(0.3)
                        break
            self.win.flip()

    def check_correctness(self, probe_image_path, is_target_probed, is_practice = False):
        """
        Checks if the clicked image matches the identity of the probed object.
        """
        distractor_icon = "images/0a.png"
        
        if is_target_probed:
            # Must match the exact image path of the probed target
            self.correct = (self.clicked_object == probe_image_path)
        else:
            # If a distractor was probed, the participant must click the '0a.png' icon
            self.correct = (self.clicked_object == distractor_icon)

        # Generate feedback
        if not is_practice:
            # Short feedback in main experiment part
            self.feedback = "Dobrze." if self.correct else "Źle."
        else:
            # Verbose feedback for training mode
            if self.clicked_object:
                clicked_cross = (self.clicked_object == distractor_icon)
                clicked_target = (self.clicked_object == probe_image_path)

                if is_target_probed:
                    if clicked_target:
                        self.feedback = "Dobrze. Został podświetlony target. Wybrałeś poprawny target."
                    elif clicked_cross:
                        self.feedback = "Źle. Został podświetlony target. Wybrałeś ikonę dystraktora."
                    else:
                        self.feedback = "Źle. Został podświetlony target. Wybrałeś zły target."
                else:  # Highlighted distractor
                    if clicked_cross:
                        self.feedback = "Dobrze. Został podświetlony dystraktor. Wybrałeś ikonę dystraktora."
                    else:
                        self.feedback = "Źle. Został podświetlony dystraktor. Nie wybrałeś ikony dystraktora."
            else:
                self.feedback = "Źle. Brak odpowiedzi."

        return self.correct
