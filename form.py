from psychopy import core, gui
import re
import uuid

class Form:
    def __init__(self):
        self.id = uuid.uuid4()
        self.email = ""
        self.sex = ""
        self.age = 0
        self.handedness = ""
        self.datetime = ""
        self.first_name = ""
        self.last_name = ""

    def show_form(self):
        while True:
            # Tworzenie formularza
            form = gui.Dlg(title="Dane uczestnika")
            form.addText("Wprowadź swoje dane:")
            form.addField("Imię* :")
            form.addField("Nazwisko* :")
            form.addField("Wiek* :")
            form.addField("Płeć (M/F)* :")
            form.addField("Prawo/leworęczny:")
            form.addField("Email* :")

            # Wyświetlanie formularza
            form_data = form.show()

            # Sprawdzanie, czy użytkownik nie anulował formularza
            if form.OK:
                self.first_name = form_data[0]
                self.last_name = form_data[1]
                self.age = form_data[2]
                self.sex = form_data[3]
                self.handedness = form_data[4]
                self.email = form_data[5]

                # Walidacja adresu e-mail za pomocą wyrażeń regularnych (regex)
                if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
                    error_dialog = gui.Dlg(title="Błąd")
                    error_dialog.addText("Nieprawidłowy adres e-mail.")
                    error_dialog.show()
                    continue

                # Sprawdzanie, czy wszystkie pola są uzupełnione
                if not all([self.email, self.first_name, self.last_name, self.handedness, self.sex, self.age]):
                    error_dialog = gui.Dlg(title="Błąd")
                    error_dialog.addText("Wszystkie pola muszą być uzupełnione.")
                    error_dialog.show()
                    continue

                break
            else:
                core.quit()
