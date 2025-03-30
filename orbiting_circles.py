from psychopy import core, visual
import numpy as np
import random
from orbiting_objects import OrbitingObjects
from orbiting_circle_pair import OrbitingCirclePair

class OrbitingCircles(OrbitingObjects):
    def __init__(self, win, target_set_size, targets, target_side, orbit_radius=0.05, speed=2.0):
        super().__init__(win, target_set_size, targets, target_side, orbit_radius, speed)
        
        self.orbits = []
        for offset in self.offsets:
            initial_angle = np.random.uniform(0, 2 * np.pi)
            dir = random.choice([-1, 1])
            pair = OrbitingCirclePair(win, offset, orbit_radius, initial_angle, dir)
            self.orbits.append(pair)
        self.targets = targets
