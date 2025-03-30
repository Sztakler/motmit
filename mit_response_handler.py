from psychopy import core, event, visual
import math

class MITResponseHandler:
    def __init__(self, win, images_paths=None):
        """
        Initialize the ResponseHandler instance.
        """
        self.win = win
        self.response = None
        self.feedback = "Incorrect. No response provided."
        self.correct = None
        self.clicked_item = None
        self.carousel_radius = 0.3
        self.items = []
        self.images_paths = images_paths[:12]

    def get_response(self):
        mouse = event.Mouse(win=self.win)

        self.draw_carousel()
        # Sorting the items based on their image names
        # Assuming the image names are in the format "images/0.png", "images/1.png", etc.
        self.items.sort(key=lambda item: int(item.image.split('/')[1].split('.')[0]))

        timer = core.Clock()
        mouse.setPos((0, 0))  # Reset mouse position
        while not self.clicked_item and timer.getTime() < 3:
            for item in self.items:
                if mouse.isPressedIn(item):
                    highlight_circle = visual.Circle(self.win, radius=0.04, fillColor=None, lineColor='lightgreen', lineWidth=4)
                    highlight_circle.pos = item.pos
                    self.clicked_item = item.image
                    item.draw()
                    highlight_circle.draw()
                    self.win.flip()  # Odświeżenie okna, aby wyświetlić highlight_circle natychmiast
                    core.wait(0.5)
                    break
                if self.clicked_item:
                    break
    
    def check_correctness(self, highlight_target, targets, objects):
        """
        Check the correctness of the response.

        Returns:
            bool: True if the response is correct, False otherwise.
        """
        
        # Checking the correctness of the response

        clicked_target = False
        for target in targets:
            if self.clicked_item == objects.images_paths[target.orbit_index]:
                clicked_target = True
                break

        if self.clicked_item:
            if clicked_target:
                if highlight_target:
                    self.feedback = "Poprawnie! Podświetlono cel."
                    self.correct = True
                else:
                    self.feedback = "Niepoprawnie. Podświetlono dystraktor."
                    self.correct = False
            else:
                if not highlight_target:
                    self.feedback = "Poprawnie! Podświetlono dystraktor."
                    self.correct = True
                else:
                    self.feedback = "Niepoprawnie. Podświetlono cel."
                    self.correct = False
                
        else:
            self.correct = False
        
        return self.correct
    
    def display_feedback(self):
        feedback_duration = 1.5 
        feedback_message = visual.TextStim(self.win, text=self.feedback, color='black')
        feedback_message.draw()
        self.win.flip()
        core.wait(feedback_duration)


    def draw_carousel(self):
        positions = self.get_circle_positions(self.carousel_radius, len(self.images_paths) + 1)
        cross = visual.ImageStim(self.win, image="images/0.png", pos=positions[0], size=(0.04, 0.04)) 
        cross.draw()     
        self.items.append(cross)
        for i, pos in enumerate(positions[1:], 1):
            item = visual.ImageStim(self.win, image=self.images_paths[i % len(self.images_paths)], pos=pos, size=(0.15, 0.15))
            item.draw()
            self.items.append(item)
        self.win.flip()
    
    def get_circle_positions(self, radius, count):
        return [(radius * math.cos(2 * math.pi * i / count + math.pi / 2),
                 radius * math.sin(2 * math.pi * i / count + math.pi / 2)) for i in range(count)]