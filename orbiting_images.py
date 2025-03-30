from psychopy import core, visual
import numpy as np
import random
from orbiting_objects import OrbitingObjects
from orbiting_images_pair import OrbitingImagesPair
from target import Target
import math

class OrbitingImages(OrbitingObjects):
    def __init__(self, win, target_set_size, targets, target_side, orbit_radius=0.05, speed=2.0, images_paths=None):
        super().__init__(win, target_set_size, targets, target_side, orbit_radius, speed)

        print("Images paths:", images_paths)
        self.images_paths = images_paths[:self.number_of_pairs]
        random.shuffle(self.images_paths)
        self.orbits = []

        # Create pairs of images for the first half of the offsets
        for i, offset in enumerate(self.offsets[:self.number_of_pairs // 2]):
            n = 2 * i
            initial_angle = np.random.uniform(0, 2 * np.pi)
            dir = random.choice([-1, 1])
            pair = OrbitingImagesPair(win, offset, self.orbit_radius, initial_angle, dir,  images_paths=self.images_paths[n:n+2])
            self.orbits.append(pair)
        
        # Create the second half of the orbits with mirrored images
        for i, offset in enumerate(self.offsets[self.number_of_pairs // 2:]):
            n = 2 * i
            initial_angle = np.random.uniform(0, 2 * np.pi)
            dir = random.choice([-1, 1])
            pair = OrbitingImagesPair(win, offset, self.orbit_radius, initial_angle, dir,  images_paths=self.images_paths[n:n+2])
            self.orbits.append(pair)

    def cover(self):
        for orbit in self.orbits:
            orbit.cover()
