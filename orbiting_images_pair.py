from orbiting_pair import OrbitingPair
from psychopy import visual

class OrbitingImagesPair(OrbitingPair):
    def __init__(self, win, offset, orbit_radius=0.1, initial_angle=0, direction=1, images_paths=None):
        super().__init__(win, offset, orbit_radius, initial_angle, direction)
        self.images_paths = images_paths
        self.covers = [visual.Circle(win, radius=0.04, fillColor='black', lineColor='black', lineWidth=4) for _ in range(2)]
        self.objects = [visual.ImageStim(win, image=path, size=(0.15, 0.15)) for path in images_paths]
        self.target_border.radius = 0.04
        self.mirror_border.radius = 0.04
        
    def cover(self):
        for i in range(2):
            self.covers[i].pos = self.objects[i].pos
            self.covers[i].draw()
