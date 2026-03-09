
from psychopy import visual

class FixationCross:
    def __init__(self, win, size):
        self.lines = [
            visual.Line(win, start=(-size, 0), end=(size, 0), lineColor='black', lineWidth=2),
            visual.Line(win, start=(0, -size), end=(0, size), lineColor='black', lineWidth=2)
        ]
    
    def draw(self):
        for line in self.lines:
            line.draw()