from psychopy import core, visual
import numpy as np
import random
from orbiting_objects import OrbitingObjects
from orbiting_circle_pair import OrbitingCirclePair
from config import scale, orbiting_speed

class OrbitingCircles(OrbitingObjects):
    def __init__(self, win, target_set_size, targets, target_side, orbit_radius=0.08 * scale, speed=orbiting_speed):
        super().__init__(win, target_set_size, targets, target_side, orbit_radius, speed)
        
        self.orbits = []
        for offset in self.offsets:
            initial_angle = np.random.uniform(0, 2 * np.pi)
            dir = random.choice([-1, 1])
            pair = OrbitingCirclePair(win, offset, orbit_radius, initial_angle, dir)
            self.orbits.append(pair)
        self.targets = targets
