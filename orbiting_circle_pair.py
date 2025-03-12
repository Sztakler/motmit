from orbiting_pair import OrbitingPair
from psychopy import visual
import numpy as np

class OrbitingCirclePair(OrbitingPair):
    def __init__(self, win, offset, orbit_radius=0.1, initial_angle=0, direction=1):
        super().__init__(win, offset, orbit_radius, initial_angle, direction)
        self.object1 = visual.Circle(win, radius=0.05, fillColor='black', lineColor='black', lineWidth=4)
        self.object2 = visual.Circle(win, radius=0.05, fillColor='black', lineColor='black', lineWidth=4)

    
