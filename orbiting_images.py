import numpy as np
import random
from orbiting_objects import OrbitingObjects
from orbiting_images_pair import OrbitingImagesPair
from config import scale, orbiting_speed

class OrbitingImages(OrbitingObjects):
    def __init__(self, win, target_set_size, targets, target_side, orbit_radius=0.05 * scale, speed=orbiting_speed, images_paths=None):
        super().__init__(win, target_set_size, targets, target_side, orbit_radius, speed)

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

    def highlight_object(self, highlight_target):
        highlighted_indices = None
        target_indices = [(target.orbit_index, target.circle_index) for target in self.targets]
        indices = [(orbit_index, circle_index) for orbit_index in range(self.number_of_pairs // 2 * self.target_side, self.number_of_pairs // 2 * (1 + self.target_side)) for circle_index in [0,1]]

        if highlight_target:
            highlighted_indices = random.choice(target_indices)
        else:
            non_target_indices = [index for index in indices if index not in target_indices]
            highlighted_indices = random.choice(non_target_indices)
            
        self.orbits[highlighted_indices[0]].highlight_target(highlighted_indices[1])
        

        return highlighted_indices
