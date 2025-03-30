from psychopy import core, visual, event
import random
import csv
from fixation_cross import FixationCross

class Form():
    def __init__(self):
        pass

class Trial:
    def __init__(self, win, trial_number, target_set_size, targets, targets_side, form, trial_type, highlight_target):
        self.win = win
        self.trial_number = trial_number
        self.orbit_radius = 0.1
        self.speed = 0.5
        self.target_set_size = target_set_size
        self.targets = targets
        self.targets_side = targets_side
        self.form = form
        self.trial_type = trial_type
        self.cross = FixationCross(win, size=0.05)
        self.interrupted = False
        self.highlight_target = highlight_target
        self.response_handler = None
        self.highlighted_indices = None
      
    def split_time(self, time, n):
        cuts = sorted([random.uniform(0, time) for _ in range(n - 1)])
        intervals = [cuts[0]] + [cuts[i] - cuts[i-1] for i in range(1, n-1)] + [time - cuts[-1]]
        return intervals

    def draw_fixation_cross(self):
        self.cross.draw()

    def draw_fixation(self):
        self.draw_fixation_cross()
        self.win.flip()
        core.wait(0.5)

    def draw_cue(self):
        delay = 0.75
        start_time = core.getTime()
        self.objects.draw_static(start_time)
        self.objects.highlight_target()
        self.win.flip()
        core.wait(delay)

    def draw_stop(self):
        delay = 0.5
        self.objects.draw_static(core.getTime())
        self.draw_fixation_cross()
        self.win.flip()
        core.wait(delay)

    def draw_probe(self):
        delay = 0.5
        self.draw_fixation_cross()
        self.objects.draw_static(core.getTime())
        self.highlighted_indices = self.objects.highlight_object(self.highlight_target)
        self.win.flip()
        core.wait(delay)

    def draw_tracking(self):
        initial_direction_movement_time = 1.0
        change_direction_time = 0.75
        new_direction_movement_time = 0.75

        start_time = core.getTime()
        while core.getTime() - start_time < initial_direction_movement_time:
            self.objects.animate(start_time)
            self.draw_fixation_cross()      
            self.win.flip()
            if 'escape' in event.getKeys():
                core.quit()

        current_time = core.getTime() - start_time
        self.objects.update_initial_angles(current_time)
        intervals = self.split_time(change_direction_time, self.objects.number_of_pairs)
        indexes = list(range(self.objects.number_of_pairs))
        random.shuffle(indexes)
        clock = core.Clock()
        for interval, index in zip(intervals, indexes):
            start_time = core.getTime()
            clock.reset()
            while clock.getTime() < interval:
                self.objects.animate(start_time)
                self.draw_fixation_cross()      
                self.win.flip()
                if 'escape' in event.getKeys():
                    core.quit()
            current_time = core.getTime() - start_time
            self.objects.update_initial_angles(current_time)
            self.objects.orbits[index].change_direction()
        
        start_time = core.getTime()
        while core.getTime() - start_time < new_direction_movement_time:
            self.objects.animate(start_time)
            self.draw_fixation_cross()     
            self.win.flip()
            if 'escape' in event.getKeys():
                core.quit()

    def run(self):
        t1 = core.getTime()
        self.draw_fixation_cross()
        self.draw_cue()
        self.draw_tracking()
        self.draw_stop()
        self.draw_probe()

        self.response_handler.get_response()
        is_correct = self.response_handler.check_correctness(self.highlight_target)
        self.response_handler.display_feedback()
        
        self.save_data(self.response_handler.clicked_circle, is_correct)
    
        t2 = core.getTime()

        print("Time:", t2 - t1)

        self.wait_for_input()

    def wait_for_input(self):   
        while True:
            keys = event.getKeys()
            if 'escape' in keys:
                core.quit()
            if keys:
                break

    def save_data(self, response, correct):
        with open('experiment_data.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            self.form = Form()
            self.form.email = "mail",
            self.form.gender= "gender",
            self.form.first_name= "name",
            self.form.last_name=  "surname"
            

            orbit_index = self.highlighted_indices[0]
            circle_index = self.highlighted_indices[1]

            writer.writerow([self.trial_number, self.trial_type, self.target_set_size, orbit_index, circle_index, correct, self.form.email, self.form.gender, self.form.first_name, self.form.last_name])

class FixationCross:
    def __init__(self, win, size):
        self.lines = [
            visual.Line(win, start=(-size, 0), end=(size, 0), lineColor='black', lineWidth=2),
            visual.Line(win, start=(0, -size), end=(0, size), lineColor='black', lineWidth=2)
        ]
    
    def draw(self):
        for line in self.lines:
            line.draw()