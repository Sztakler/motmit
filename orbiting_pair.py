from psychopy import visual
import numpy as np
from config import scale, target_color, mirror_color

class OrbitingPair:
    def __init__(self, win, offset, orbit_radius=0.1 * scale, initial_angle=0, direction=1):
        self.win = win
        self.orbit_radius = orbit_radius
        self.offset = offset
        self.initial_angle = initial_angle
        self.direction = direction
        self.angle = 0
        self.line_width = 8
        self.target_border = visual.Circle(win, radius=0.025 * scale, fillColor=None, lineColor=target_color, lineWidth=self.line_width)
        self.mirror_border = visual.Circle(win, radius=0.025 * scale, fillColor=None, lineColor=mirror_color, lineWidth=self.line_width)
        self.objects = []

    def draw_static(self):
        x1 = self.orbit_radius * np.cos(self.angle + self.initial_angle) + self.offset[0]
        y1 = self.orbit_radius * np.sin(self.angle + self.initial_angle) + self.offset[1]
        x2 = self.orbit_radius * np.cos(self.angle + np.pi + self.initial_angle) + self.offset[0]
        y2 = self.orbit_radius * np.sin(self.angle + np.pi + self.initial_angle) + self.offset[1]
        
        self.objects[0].pos = (x1, y1)
        self.objects[1].pos = (x2, y2)
        
        self.objects[0].draw()
        self.objects[1].draw()

    def update_angle(self, t, speed):
        self.angle = self.direction * t * speed

    def animate(self, t, speed):
        self.update_angle(t, speed)
        x1 = self.orbit_radius * np.cos(self.angle + self.initial_angle) + self.offset[0]
        y1 = self.orbit_radius * np.sin(self.angle + self.initial_angle) + self.offset[1]
        x2 = self.orbit_radius * np.cos(self.angle + np.pi + self.initial_angle) + self.offset[0]
        y2 = self.orbit_radius * np.sin(self.angle + np.pi + self.initial_angle) + self.offset[1]
        
        self.objects[0].pos = (x1, y1)
        self.objects[1].pos = (x2, y2)
        
        self.objects[0].draw()
        self.objects[1].draw()

    def highlight_target(self, index):
        self.target_border.lineWidth = self.line_width
        self.target_border.pos = self.objects[index].pos
        self.target_border.draw()


    def highlight_mirror(self, index):
        self.mirror_border.lineWidth = self.line_width
        self.mirror_border.pos = self.objects[index].pos
        self.mirror_border.draw()

    def reset_highlight(self):
        self.target_border.lineWidth = 0
        self.mirror_border.lineWidth = 0

    def change_direction(self):
        self.direction *= -1

    def update_initial_angle(self, t, speed):
        self.initial_angle += self.direction * speed * t