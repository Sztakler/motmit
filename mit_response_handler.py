from psychopy import core, event, visual
import math
from response_handler import ResponseHandler

class MITResponseHandler(ResponseHandler):
    def __init__(self, win, images_paths=None):
        """
        Initialize the ResponseHandler instance.
        """
        super().__init__(win)
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
        while not self.clicked_object and timer.getTime() < 3:
            for item in self.items:
                if mouse.isPressedIn(item):
                    highlight_circle = visual.Circle(self.win, radius=0.04, fillColor=None, lineColor='lightgreen', lineWidth=4)
                    highlight_circle.pos = item.pos
                    self.clicked_object = item.image
                    item.draw()
                    highlight_circle.draw()
                    self.win.flip()  # Odświeżenie okna, aby wyświetlić highlight_circle natychmiast
                    core.wait(0.5)
                    break
                if self.clicked_object:
                    break
    
    def check_correctness(self, highlight_target, targets, highlighted_indices, objects):
        """
        Check the correctness of the response.

        Returns:
            bool: True if the response is correct, False otherwise.
        """

        highlighted_image = objects.images_paths[highlighted_indices[0]]
        clicked_target = self.clicked_object == highlighted_image
        clicked_cross = self.clicked_object == objects.images_paths[0]

        if self.clicked_object:
            if highlight_target:
                if clicked_target:
                    self.feedback = "Poprawnie! To był cel."
                    self.correct = True
                else:
                    self.feedback = "Niepoprawnie. To nie był cel."
                    self.correct = False
            else:
                if clicked_cross:
                    self.feedback = "Poprawnie! Podświetlono dystraktor."
                    self.correct = True
                else:   
                    self.feedback = "Niepoprawnie. Podświetlono cel."
                    self.correct = False
        else:
            self.correct = False

        return self.correct

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