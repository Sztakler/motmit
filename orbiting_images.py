import numpy as np
import random
from orbiting_objects import OrbitingObjects
from orbiting_images_pair import OrbitingImagesPair
from config import scale, orbiting_speed, images_orbit_radius, mot_target_color

class OrbitingImages(OrbitingObjects):
    def __init__(self, win, target_set_size, targets, target_side, orbit_radius=images_orbit_radius * scale, speed=orbiting_speed, images_paths=None, target_color=mot_target_color):
        super().__init__(win, target_set_size, targets, target_side, orbit_radius, speed)

        self.images_paths = images_paths[:self.number_of_pairs // 2]
        random.shuffle(self.images_paths)
        self.orbits = []

        # Create pairs of images for the first half of the offsets
        for i, offset in enumerate(self.offsets[:self.number_of_pairs // 2]):
            initial_angle = np.random.uniform(0, 2 * np.pi)
            dir = random.choice([-1, 1])
            pair = OrbitingImagesPair(win, offset, self.orbit_radius, initial_angle, dir, images_paths=self.images_paths[i], target_color=target_color)
            self.orbits.append(pair)
        
        # Create the second half of the orbits with mirrored images
        for i, offset in enumerate(self.offsets[self.number_of_pairs // 2:]):
            initial_angle = np.random.uniform(0, 2 * np.pi)
            dir = random.choice([-1, 1])
            pair = OrbitingImagesPair(win, offset, self.orbit_radius, initial_angle, dir,  images_paths=self.images_paths[i], target_color=target_color)
            self.orbits.append(pair)
        
        print("Orbits:", len(self.orbits))

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
