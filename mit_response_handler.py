from psychopy import core, event, visual
import math
from config import scale, mit_target_color, image_radius, max_response_time_mit

from response_handler import ResponseHandler
from logger import logger

def sort_key(image_path):
        filename = image_path.split('/')[-1].split('.')[0]
        num = int(filename[:-1])
        letter = filename[-1]
        return (num, letter)

class MITResponseHandler(ResponseHandler):
    def __init__(self, win, images_paths=None):
        """
        Initialize the ResponseHandler instance.
        """
        super().__init__(win)
        self.carousel_radius = 0.3 * scale
        self.items = []
        self.image_pairs = images_paths

    def get_response(self, objects):
        mouse = event.Mouse(win=self.win)

        self.draw_carousel(objects)

        timer = core.Clock()
        mouse.setPos((0, 0))  # Reset mouse position
        while not self.clicked_object and timer.getTime() < max_response_time_mit:
            for item in self.items:
                if mouse.isPressedIn(item):
                    highlight_circle = visual.Circle(self.win, radius=0.04 * scale, fillColor=None, lineColor=mit_target_color, lineWidth=4)
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
        logger.info(f"Check correctness: highlight_target {highlight_target}, targets {targets}, highlighted_indices {highlighted_indices}, objects {objects}")
        highlighted_image = objects.images_paths[highlighted_indices[0] % 3][highlighted_indices[1]]
        clicked_target = self.clicked_object == highlighted_image
        clicked_cross = self.clicked_object == "images/0a.png"

        if self.clicked_object:
            if highlight_target:
                if clicked_target:
                    self.feedback = "Dobrze."
                    self.correct = True
                else:
                    self.feedback = "Źle."
                    self.correct = False
            else:
                if clicked_cross:
                    self.feedback = "Dobrze."
                    self.correct = True
                else:   
                    self.feedback = "Źle."
                    self.correct = False
        else:
            self.correct = False

        return self.correct
    
    def check_correctness_training(self, highlight_target, targets, highlighted_indices, objects):
        """
        Check the correctness of the response and provide verbose feedback.

        Returns:
            bool: True if the response is correct, False otherwise.
        """
        logger.info(f"Check correctness: highlight_target {highlight_target}, targets {targets}, highlighted_indices {highlighted_indices}, objects {objects}")
        highlighted_image = objects.images_paths[highlighted_indices[0] % 3][highlighted_indices[1]]
        clicked_target = self.clicked_object == highlighted_image
        clicked_cross = self.clicked_object == "images/0a.png"

        if self.clicked_object:
            if highlight_target:
                if clicked_target:
                    self.feedback = "Dobrze. Został podświetlony target. Wybrałeś poprawny target."
                    self.correct = True
                elif clicked_cross:
                    self.feedback = "Źle. Został podświetlony target. Wybrałeś ikonę dystraktora."
                    self.correct = False
                else:
                    self.feedback = "Źle. Został podświetlony target. Wybrałeś zły target."
                    self.correct = False
            else:
                if clicked_cross:
                    self.feedback = "Dobrze. Został podświetlony dystraktor. Wybrałeś ikonę dystraktora."
                    self.correct = True
                else:   
                    self.feedback = "Źle. Został podświetlony dystraktor. Nie wybrałeś ikony dystraktora."
                    self.correct = False
        else:
            self.correct = False

        print(self.feedback)
        return self.correct

    def draw_carousel(self, objects):
        flat_images = [img for pair in objects.images_paths for img in pair]

        flat_images.sort(key=sort_key)
        positions = self.get_circle_positions(self.carousel_radius, len(flat_images) + 1)
        
        cross = visual.ImageStim(self.win, image="images/0a.png", pos=positions[0], size=(image_radius * scale, image_radius * scale)) 
        cross.draw()     
        self.items.append(cross)
        
        for i, (image_path, pos) in enumerate(zip(flat_images, positions[1:]), 1):
            item = visual.ImageStim(self.win, image=image_path, pos=pos, size=(image_radius * scale, image_radius * scale))
            item.draw()
            self.items.append(item)
        
        self.win.flip()
    
    def get_circle_positions(self, radius, count):
        return [(radius * math.cos(2 * math.pi * i / count + math.pi / 2),
                 radius * math.sin(2 * math.pi * i / count + math.pi / 2)) for i in range(count)]
