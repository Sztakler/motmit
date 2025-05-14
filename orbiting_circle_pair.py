from orbiting_pair import OrbitingPair
from psychopy import visual

from config import scale, mot_target_color

class OrbitingCirclePair(OrbitingPair):
    def __init__(self, win, offset, orbit_radius=0.1 * scale, initial_angle=0, direction=1, target_color=mot_target_color):
        super().__init__(win, offset, orbit_radius, initial_angle, direction, target_color)
        self.objects = [visual.Circle(win, radius=0.025 * scale, fillColor='black', lineColor='black', lineWidth=4),
                        visual.Circle(win, radius=0.025 * scale, fillColor='black', lineColor='black', lineWidth=4)]

    
