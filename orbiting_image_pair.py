from psychopy import visual
import numpy as np

class OrbitingImagePair:
    def __init__(self, win, offset, images_paths, orbit_radius=0.1, initial_angle=0, direction=1):
        self.win = win
        self.orbit_radius = orbit_radius
        self.offset = offset
        self.initial_angle = initial_angle
        self.direction = direction
        self.image1 = visual.ImageStim(win, image=images_paths[0], size=(0.25, 0.25))
        self.image2 = visual.ImageStim(win, image=images_paths[1], size=(0.25, 0.25))
        self.covers = [visual.Circle(win, radius=0.08, fillColor='black', lineColor='black', lineWidth=4) for _ in range(2)]
        self.highlight_circle = visual.Circle(win, radius=0.08, fillColor=None, lineColor='red', lineWidth=4)
        self.highlight_mirror_circle = visual.Circle(win, radius=0.08, fillColor=None, lineColor='red', lineWidth=2)
        self.angle = 0

    def draw_static(self):
        x1 = self.orbit_radius * np.cos(self.angle + self.initial_angle) + self.offset[0]
        y1 = self.orbit_radius * np.sin(self.angle + self.initial_angle) + self.offset[1]
        x2 = self.orbit_radius * np.cos(self.angle + np.pi + self.initial_angle) + self.offset[0]
        y2 = self.orbit_radius * np.sin(self.angle + np.pi + self.initial_angle) + self.offset[1]
        
        self.image1.pos = (x1, y1)
        self.image2.pos = (x2, y2)
        
        self.image1.draw()
        self.image2.draw()

    def update_angle(self, t, speed):
        self.angle = self.direction * t * speed

    def animate(self, t, speed):
        self.update_angle(t, speed)
        x1 = self.orbit_radius * np.cos(self.angle + self.initial_angle) + self.offset[0]
        y1 = self.orbit_radius * np.sin(self.angle + self.initial_angle) + self.offset[1]
        x2 = self.orbit_radius * np.cos(self.angle + np.pi + self.initial_angle) + self.offset[0]
        y2 = self.orbit_radius * np.sin(self.angle + np.pi + self.initial_angle) + self.offset[1]
        
        self.image1.pos = (x1, y1)
        self.image2.pos = (x2, y2)
        
        self.image1.draw()
        self.image2.draw()

    def highlight_target(self, circle_index):
        if circle_index == 0:
            self.highlight_circle.pos = self.image1.pos
        else:
            self.highlight_circle.pos = self.image2.pos
        self.highlight_circle.draw()

    def highlight_mirror(self, circle_index):
        if circle_index == 0:
            self.highlight_mirror_circle.pos = self.image1.pos
        else:
            self.highlight_mirror_circle.pos = self.image2.pos
        self.highlight_mirror_circle.draw()

    def reset_highlight(self, circle_index):
        if circle_index == 0:
            self.image1.lineColor = 'black'
            self.image1.lineWidth = 4
        else:
            self.image2.lineColor = 'black'
            self.image2.lineWidth = 4

    def change_direction(self):
        self.direction *= -1

    def update_initial_angle(self, t, speed):
        self.initial_angle += self.direction * speed * t

    def cover_elements(self):
        for cover in self.covers:
            cover.pos = self.image1.pos
            cover.draw()
            cover.pos = self.image2.pos
            cover.draw()