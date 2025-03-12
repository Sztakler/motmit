from psychopy import visual, core, event
import random
import math
import numpy as np
from orbiting_image_pair import OrbitingImagePair
from target import Target

class OrbitingImages:
    def __init__(self, win, target_set_size, targets, target_side, images_paths):
        self.win = win
        self.target_set_size = target_set_size
        self.target_side = target_side
        self.orbit_radius = 0.1
        self.carousel_radius = 0.6
        self.speed = 0.5
        self.random_orbit_index = 0
        self.random_circle = 0
        self.highlighted_target = False
        self.circle_pairs = []
        self.number_of_pairs = 6
        offsets = self.get_offsets()
           
        self.images_paths = images_paths[:]
        random.shuffle(self.images_paths)
        self.images_paths = self.images_paths[:self.number_of_pairs * 2]
        for i, offset in enumerate(offsets):
            initial_angle = np.random.uniform(0, 2 * np.pi)  # Losowy kąt początkowy
            dir = random.choice([-1, 1]) # Losowy kierunek
            n = 2 * i
            print("pairs,", self.images_paths[n:n+2])
            pair = OrbitingImagePair(win, offset, self.images_paths[n:n+2], self.orbit_radius, initial_angle, dir)
            self.circle_pairs.append(pair)

        self.targets = targets

    def get_offsets(self):
        return [(-0.6, 0.5), (-0.6, 0.0), (-0.6, -0.5),
                    (0.6, 0.5),  (0.6, 0.0),  (0.6, -0.5)]

    def get_circle_positions(self, radius, count):
        return [(radius * math.cos(2 * math.pi * i / count + math.pi / 2),
                 radius * math.sin(2 * math.pi * i / count + math.pi / 2)) for i in range(count)]

    def highlight_target(self):
        for target in self.targets:
            self.circle_pairs[target.orbit_index].highlight_target(target.circle_index)
            self.circle_pairs[target.mirror_orbit_index].highlight_mirror(target.circle_index)

    def highlight_random_element(self):
        available_orbit_indices = list(range(self.number_of_pairs // 2 * self.target_side, self.number_of_pairs // 2 * (1 + self.target_side)))
        self.random_orbit_index = random.choice(available_orbit_indices)
        self.random_circle = random.randint(0, 1)
        self.circle_pairs[self.random_orbit_index].highlight_target(self.random_circle)
        
        self.highlighted_target = False
        self.check_highlighted_element()

    def check_highlighted_element(self):
        self.highlighted_target = False
        for target in self.targets:
            if self.random_orbit_index == target.orbit_index and self.random_circle == target.circle_index:
                self.highlighted_target = True
            

    def reset_target(self):
        for target in self.targets:
            self.circle_pairs[target.orbit_index].reset_highlight(target.circle_index)
            self.circle_pairs[target.mirror_orbit_index].reset_highlight(target.circle_index) 
        self.circle_pairs[self.random_orbit_index].reset_highlight(target.circle_index)

    def change_direction(self, t):
        for pair in self.circle_pairs:
            pair.update_initial_angle(t, self.speed)
            pair.change_direction()
        
    def draw_static(self):
        for pair in self.circle_pairs:
            pair.draw_static()

    def animate(self, start_time):
        t = core.getTime() - start_time
        self.reset_target()
        for pair in self.circle_pairs:
            pair.animate(t, self.speed)

    def is_target_highlighted(self):
        return self.highlighted_target

    def cover_elements(self):
        for pair in self.circle_pairs:
            pair.cover_elements()

    def draw_carousel(self):
        positions = self.get_circle_positions(self.carousel_radius, len(self.images_paths) + 1)
        images = []
        cross = visual.ImageStim(self.win, image="snowflakes/0.png", pos=positions[0], size=(0.1, 0.1)) 
        cross.draw()     
        images.append(cross)
        for i, pos in enumerate(positions[1:], 1):
            image = visual.ImageStim(self.win, image=self.images_paths[i % len(self.images_paths)], pos=pos, size=(0.4, 0.4))
            image.draw()
            images.append(image)
        self.win.flip()
        return images