from orbiting_pair import OrbitingPair
from psychopy import visual
from config import scale, image_radius, image_cover_radius, mit_target_color

class OrbitingImagesPair(OrbitingPair):
    def __init__(self, win, offset, orbit_radius=0.15 * scale, initial_angle=0, direction=1, images_paths=None, target_color=mit_target_color):
        super().__init__(win, offset, orbit_radius, initial_angle, direction, target_color)
        self.images_paths = images_paths
        self.covers = [visual.Circle(win, radius=image_cover_radius * scale, fillColor='black', lineColor='black', lineWidth=4) for _ in range(2)]
        self.objects = [visual.ImageStim(win, image=path, size=(image_radius * scale, image_radius * scale)) for path in images_paths]
        self.target_border.radius = image_cover_radius * scale
        self.mirror_border.radius = image_cover_radius * scale
        
    def cover(self):
        for i in range(2):
            self.covers[i].pos = self.objects[i].pos
            self.covers[i].draw()
