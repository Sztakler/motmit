from psychopy import visual
import numpy as np

class OrbitingPair:
    def __init__(self, win, offset, orbit_radius=0.1, initial_angle=0, direction=1):
        self.win = win
        self.orbit_radius = orbit_radius
        self.offset = offset
        self.initial_angle = initial_angle
        self.direction = direction
        self.angle = 0

    def draw_static(self):
        x1 = self.orbit_radius * np.cos(self.angle + self.initial_angle) + self.offset[0]
        y1 = self.orbit_radius * np.sin(self.angle + self.initial_angle) + self.offset[1]
        x2 = self.orbit_radius * np.cos(self.angle + np.pi + self.initial_angle) + self.offset[0]
        y2 = self.orbit_radius * np.sin(self.angle + np.pi + self.initial_angle) + self.offset[1]
        
        self.object1.pos = (x1, y1)
        self.object2.pos = (x2, y2)
        
        self.object1.draw()
        self.object2.draw()

    def update_angle(self, t, speed):
        self.angle = self.direction * t * speed

    def animate(self, t, speed):
        self.update_angle(t, speed)
        x1 = self.orbit_radius * np.cos(self.angle + self.initial_angle) + self.offset[0]
        y1 = self.orbit_radius * np.sin(self.angle + self.initial_angle) + self.offset[1]
        x2 = self.orbit_radius * np.cos(self.angle + np.pi + self.initial_angle) + self.offset[0]
        y2 = self.orbit_radius * np.sin(self.angle + np.pi + self.initial_angle) + self.offset[1]
        
        self.object1.pos = (x1, y1)
        self.object2.pos = (x2, y2)
        
        self.object1.draw()
        self.object2.draw()

    def highlight_target(self, index):
        if index == 0:
            self.object1.lineColor = 'red'
        else:
            self.object2.lineColor = 'red'

    def highlight_mirror(self, index):
        if index == 0:
            self.object1.lineColor = 'red'
            self.object1.lineWidth = 2
        else:
            self.object2.lineColor = 'red'
            self.object2.lineWidth = 2

    def reset_highlight(self, index):
        if index == 0:
            self.object1.lineColor = 'black'
            self.object1.lineWidth = 4
        else:
            self.object2.lineColor = 'black'
            self.object2.lineWidth = 4

    def change_direction(self):
        self.direction *= -1

    def update_initial_angle(self, t, speed):
        self.initial_angle += self.direction * speed * t