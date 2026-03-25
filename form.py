from psychopy import core, gui
import re
import uuid

class Form:
    def __init__(self):
        self.id = str(uuid.uuid4())[:8]
        self.sex = ""
        self.age = 0
        self.handedness = ""
        self.datetime = ""

    def show_form(self):
        while True:
            form = gui.Dlg(title="Dane uczestnika")
            form.addText("Wprowadź swoje dane:")
            form.addField("Wiek* :")
            form.addField("Płeć (M/F)* :")
            form.addField("Prawo/leworęczny:")

            form_data = form.show()

            if form.OK:
                self.age = form_data[0]
                self.sex = form_data[1]
                self.handedness = form_data[2]

                if not all([self.handedness, self.sex, self.age]):
                    error_dialog = gui.Dlg(title="Błąd")
                    error_dialog.addText("Wszystkie pola muszą być uzupełnione.")
                    error_dialog.show()
                    continue

                break
            else:
                core.quit()
