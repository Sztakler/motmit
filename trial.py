from psychopy import core, visual, event
import random
from orbiting_circles import OrbitingCircles
from orbiting_images import OrbitingImages
import csv

class Trial:
    def __init__(self, win, trial_number, target_set_size, targets, targets_side, form, trial_type, images_paths=None):
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
        if trial_type == 'mot':
            self.orbiting_circles = OrbitingCircles(win, self.target_set_size, self.targets, self.targets_side)
        elif trial_type == 'mit':
            self.orbiting_images = OrbitingImages(win, self.target_set_size, self.targets, self.targets_side, images_paths)

    def run(self):
        # Tworzenie krzyżyka na środku ekranu
        self.cross.draw()
        self.win.flip()
        core.wait(0.5)

        if self.trial_type == 'mot':
            # Rysowanie statycznych kółek przez 750 ms
            self.orbiting_circles.highlight_target()
            self.orbiting_circles.draw_static(core.getTime())
            # Rysowanie krzyżyka
            self.cross.draw()

            self.win.flip()
            core.wait(0.75)

            # Animacja kółek
            start_time = core.getTime()
            random_delay = 0.75 + random.uniform(0.0, 1.0)
            while core.getTime() - start_time < random_delay:
                current_time = core.getTime() - start_time
                self.orbiting_circles.animate(start_time)

                # Rysowanie krzyżyka
                self.cross.draw()
                
                self.win.flip()

            self.orbiting_circles.change_direction(current_time)
            start_time = core.getTime()
            delay = 2.5 - random_delay
            while core.getTime() - start_time < delay:
                current_time = core.getTime() - start_time
                self.orbiting_circles.animate(start_time)

                # Rysowanie krzyżyka
                self.cross.draw()
                
                self.win.flip()

            self.orbiting_circles.draw_static(current_time)
            self.cross.draw()
            self.win.flip()
            core.wait(0.5)

            # Podświetlenie losowego elementu (cel lub dystraktor)
            self.orbiting_circles.highlight_random_element()
            self.orbiting_circles.draw_static(current_time)
            self.cross.draw()
            self.win.flip()
            core.wait(0.75)

            # Resetowanie podświetlenia
            self.orbiting_circles.reset_target()
            self.win.flip()

            green_circle = visual.Circle(self.win, radius=0.2, fillColor='green', pos=(-0.4, 0))
            red_circle = visual.Circle(self.win, radius=0.2, fillColor='red', pos=(0.4, 0))

            green_circle.draw()
            red_circle.draw()
            self.win.flip()

            # Czekanie na kliknięcie w kółko
            mouse = event.Mouse(win=self.win)
            clicked_circle = None

            while not clicked_circle:
                if mouse.isPressedIn(green_circle):
                    clicked_circle = 'green'
                elif mouse.isPressedIn(red_circle):
                    clicked_circle = 'red'

            # Sprawdzanie poprawności odpowiedzi
            if clicked_circle == 'green':
                if self.orbiting_circles.is_target_highlighted():
                    feedback = "Poprawnie! Podświetlono cel."
                    correct = True
                else:
                    feedback = "Niepoprawnie. Podświetlono dystraktor."
                    correct = False
            elif clicked_circle == 'red':
                if not self.orbiting_circles.is_target_highlighted():
                    feedback = "Poprawnie! Podświetlono dystraktor."
                    correct = True
                else:
                    feedback = "Niepoprawnie. Podświetlono cel."
                    correct = False

            #Wyswietlenie feedbacku
            feedback_message = visual.TextStim(self.win, text=feedback, color='black')
            feedback_message.draw()
            self.win.flip()
            core.wait(2)

            # Zapisz dane do pliku CSV 
            self.save_data(clicked_circle, correct)

        elif self.trial_type == 'mit':
             # Rysowanie statycznych kółek przez 750 ms
            self.orbiting_images.draw_static()
            self.orbiting_images.highlight_target()
            # Rysowanie krzyżyka
            self.cross.draw()

            self.win.flip()
            core.wait(2.75)

            # Animacja obrazków
            start_time = core.getTime()
            random_delay = 0.75 + random.uniform(0.0, 1.0)
            while core.getTime() - start_time < random_delay:
                current_time = core.getTime() - start_time
                self.orbiting_images.animate(start_time)

                # Rysowanie krzyżyka
                self.cross.draw()
                
                self.win.flip()

            self.orbiting_images.change_direction(current_time)
            start_time = core.getTime()
            delay = 2.5 - random_delay
            while core.getTime() - start_time < delay:
                self.orbiting_images.animate(start_time)

                # Rysowanie krzyżyka
                self.cross.draw()
                
                self.win.flip()

            self.orbiting_images.draw_static()
            self.cross.draw()
            self.win.flip()
            core.wait(0.5)

            # Podświetlenie losowego elementu (cel lub dystraktor)
            self.orbiting_images.draw_static()
            self.orbiting_images.cover_elements()
            self.orbiting_images.highlight_random_element()
            self.cross.draw()
            self.win.flip()
            core.wait(0.75)

            # Resetowanie podświetlenia
            self.orbiting_images.reset_target()

            clicked_image = None
            images = self.orbiting_images.draw_carousel()
            images.sort(key=lambda image: int(image.image.split('/')[1].split('.')[0]))
            mouse = event.Mouse(self.win)

            while not clicked_image:
                for image in images:
                    if mouse.isPressedIn(image):
                        highlight_circle = visual.Circle(self.win, radius=0.08, fillColor=None, lineColor='red', lineWidth=4)
                        highlight_circle.pos = image.pos
                        clicked_image = image.image
                        image.draw()
                        highlight_circle.draw()
                        self.win.flip()  # Odświeżenie okna, aby wyświetlić highlight_circle natychmiast
                        core.wait(0.5)
                        break
                if clicked_image:
                    break

            clicked_target = False
            for target in self.targets:
                if clicked_image == self.orbiting_images.images_paths[target.orbit_index]:
                    clicked_target = True
                    break

            correct = False

            feedback = ""
            if clicked_image:
                if clicked_target:
                    if self.orbiting_images.is_target_highlighted():
                        feedback = "Poprawnie! Podświetlono cel."
                        correct = True
                    else:
                        feedback = "Niepoprawnie. Podświetlono dystraktor."
                        correct = False
                    print("Freedback1 : ", feedback)
                else:
                    if not self.orbiting_images.is_target_highlighted():
                        feedback = "Poprawnie! Podświetlono dystraktor."
                        correct = True
                    else:
                        feedback = "Niepoprawnie. Podświetlono cel."
                        correct = False
                    print("Freedback2 : ", feedback)
                    
            else:
                correct = False

            self.win.flip()
            #Wyswietlenie feedbacku
            feedback_message = visual.TextStim(self.win, text=feedback, color='black')
            feedback_message.draw()
            self.win.flip()
            core.wait(2)

            # Zapisanie danych do pliku CSV
            image_name = clicked_image.split('/')[1]
            self.save_data(image_name, correct)           

        self.win.flip()


    def save_data(self, response, correct):
        with open('experiment_data.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            # TODO zapisywac tylko wybrany target, a nie wszystkie
            writer.writerow([self.trial_number, self.trial_type, self.target_set_size, self.targets[0].orbit_index, response, correct, self.form.email, self.form.gender, self.form.first_name, self.form.last_name])

class FixationCross:
    def __init__(self, win, size):
        self.lines = [
            visual.Line(win, start=(-size, 0), end=(size, 0), lineColor='black', lineWidth=2),
            visual.Line(win, start=(0, -size), end=(0, size), lineColor='black', lineWidth=2)
        ]
    
    def draw(self):
        for line in self.lines:
            line.draw()