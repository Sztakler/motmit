from orbiting_pair import OrbitingPair
from psychopy import visual

class OrbitingCirclePair(OrbitingPair):
    def __init__(self, win, offset, orbit_radius=0.1, initial_angle=0, direction=1):
        super().__init__(win, offset, orbit_radius, initial_angle, direction)
        self.objects = [visual.Circle(win, radius=0.025, fillColor='black', lineColor='black', lineWidth=4),
                        visual.Circle(win, radius=0.025, fillColor='black', lineColor='black', lineWidth=4)]

    
