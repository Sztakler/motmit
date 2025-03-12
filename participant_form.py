from psychopy import core, gui
import re

class ParticipantForm:
    def __init__(self, win):
        self.win = win
        self.email = ""
        self.gender = ""
        self.first_name = ""
        self.last_name = ""

    def show_form(self):
        while True:
            # Tworzenie formularza
            form = gui.Dlg(title="Dane uczestnika")
            form.addText("Wprowadź swoje dane:")
            form.addField("Email* :")
            form.addField("Płeć (M/F)* :")
            form.addField("Imię* :")
            form.addField("Nazwisko* :")

            # Wyświetlanie formularza
            form_data = form.show()

            # Sprawdzanie, czy użytkownik nie anulował formularza
            if form.OK:
                self.email = form_data[0]
                self.gender = form_data[1]
                self.first_name = form_data[2]
                self.last_name = form_data[3]

                # Walidacja adresu e-mail za pomocą wyrażeń regularnych (regex)
                if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
                    error_dialog = gui.Dlg(title="Błąd")
                    error_dialog.addText("Nieprawidłowy adres e-mail.")
                    error_dialog.show()
                    continue

                # Sprawdzanie, czy wszystkie pola są uzupełnione
                if not all([self.email, self.gender, self.first_name, self.last_name]):
                    error_dialog = gui.Dlg(title="Błąd")
                    error_dialog.addText("Wszystkie pola muszą być uzupełnione.")
                    error_dialog.show()
                    continue

                break
            else:
                core.quit()