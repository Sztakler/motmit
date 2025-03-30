from psychopy import core, visual
import numpy as np
import random

class OrbitingObjects:
    def __init__(self, win, target_set_size, targets, target_side, orbit_radius=0.05, speed=2.0):
        self.win = win
        self.orbit_radius = orbit_radius
        self.speed = speed
        self.target_set_size = target_set_size
        self.target_side = target_side
        self.number_of_pairs = 6
        self.random_orbit_index = 0
        self.targets = targets
        self.offsets = self.get_offsets()
        self.orbits = []


    def get_offsets(self):
        return [(-0.6, 0.3), (-0.6, 0.0), (-0.6, -0.3),
                    (0.6, 0.3),  (0.6, 0.0),  (0.6, -0.3)]
    
    def highlight_target(self):
        for target in self.targets:
            self.orbits[target.orbit_index].highlight_target(target.circle_index)
            self.orbits[target.mirror_orbit_index].highlight_mirror(target.circle_index)

    def highlight_object(self, highlight_target):
        highlighted_indices = None
        target_indices = [(target.orbit_index, target.circle_index) for target in self.targets]
        # indices = [(orbit_index, circle_index) for orbit_index in range(self.number_of_pairs) for circle_index in [0,1]]
        indices = [(orbit_index, circle_index) for orbit_index in range(self.number_of_pairs // 2 * self.target_side, self.number_of_pairs // 2 * (1 + self.target_side)) for circle_index in [0,1]]


        if highlight_target:
            highlighted_indices = random.choice(target_indices)
        else:
            non_target_indices = [index for index in indices if index not in target_indices]
            highlighted_indices = random.choice(non_target_indices)
            
        self.orbits[highlighted_indices[0]].highlight_target(highlighted_indices[1])

        return highlighted_indices

    def highlight_random_element(self):
        available_orbit_indices = list(range(self.number_of_pairs // 2 * self.target_side, self.number_of_pairs // 2 * (1 + self.target_side)))
        self.random_orbit_index = random.choice(available_orbit_indices)
        self.random_circle = random.randint(0, 1)
        self.orbits[self.random_orbit_index].highlight_target(self.random_circle)
        
        self.highlighted_target = False
        self.check_highlighted_element()

    def check_highlighted_element(self):
        self.highlighted_target = False
        for target in self.targets:
            if self.random_orbit_index == target.orbit_index and self.random_circle == target.circle_index:
                self.highlighted_target = True

    def reset_target(self):
        for target in self.targets:
            self.orbits[target.orbit_index].reset_highlight()
            self.orbits[target.mirror_orbit_index].reset_highlight() 
        self.orbits[self.random_orbit_index].reset_highlight()

    def update_initial_angles(self, t):
        for pair in self.orbits:
            pair.update_initial_angle(t, self.speed)

    def change_direction(self, t):
        self.update_initial_angles(t)
        for pair in self.orbits:
            pair.change_direction()
        
    def draw_static(self, current_time):
        t = current_time
        for pair in self.orbits:
            pair.draw_static()

    def animate(self, start_time):
        t = core.getTime() - start_time
        self.reset_target()
        for pair in self.orbits:
            pair.animate(t, self.speed)

    def is_target_highlighted(self):
        return self.highlighted_target