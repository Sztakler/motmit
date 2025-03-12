from psychopy import core, visual
import numpy as np
import random
from orbiting_circle_pair import OrbitingCirclePair
from target import Target

class OrbitingCircles:
    def __init__(self, win, target_set_size, targets, target_side, orbit_radius=0.1, speed=0.5):
        self.win = win
        self.orbit_radius = orbit_radius
        self.speed = speed
        self.target_set_size = target_set_size
        self.target_side = target_side
        self.number_of_pairs = 6
        self.random_orbit_index = 0

        self.circle_pairs = []
        offsets = self.get_offsets()
        for offset in offsets:
            initial_angle = np.random.uniform(0, 2 * np.pi)  # Losowy kąt początkowy
            dir = random.choice([-1, 1]) # Losowy kierunek
            pair = OrbitingCirclePair(win, offset, orbit_radius, initial_angle, dir)
            self.circle_pairs.append(pair)


        self.targets = targets

    def get_offsets(self):
        return [(-0.6, 0.5), (-0.6, 0.0), (-0.6, -0.5),
                    (0.6, 0.5),  (0.6, 0.0),  (0.6, -0.5)]
    
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

    def update_initial_angles(self, t):
        for pair in self.circle_pairs:
            pair.update_initial_angle(t, self.speed)

    def change_direction(self, t):
        self.update_initial_angles(t)
        for pair in self.circle_pairs:
            pair.change_direction()
        
    def draw_static(self, current_time):
        t = current_time
        print(t)
        for pair in self.circle_pairs:
            pair.draw_static()

    def animate(self, start_time):
        t = core.getTime() - start_time
        self.reset_target()
        for pair in self.circle_pairs:
            pair.animate(t, self.speed)

    def is_target_highlighted(self):
        return self.highlighted_target