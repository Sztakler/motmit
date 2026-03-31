from psychopy import core, gui
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
            form.addText("Wprowadź swoje dane (pola z gwiazdką są wymagane):")
            form.addField("Wiek* :")
            form.addField("Płeć (M/F)* :")
            form.addField("Ręczność (R/L)* :")

            form_data = form.show()

            if form.OK:
                raw_age = str(form_data[0]).strip()
                raw_sex = str(form_data[1]).strip().upper()
                raw_hand = str(form_data[2]).strip().upper()

                # Get first letter of the word (mężczyzna -> M)
                clean_sex = raw_sex[0] if raw_sex else ""
                clean_hand = raw_hand[0] if raw_hand else ""

                errors = []

                # Check whether age is a number
                if not raw_age.isdigit():
                    errors.append("- Wiek musi być liczbą.")
                
                # Check sex
                if clean_sex not in ['M', 'F']:
                    errors.append("- Płeć musi zaczynać się od M (mężczyzna) lub F (kobieta).")

                # Check handedness
                if clean_hand not in ['R', 'L']:
                    errors.append("- Ręczność musi zaczynać się od R (prawo) lub L (lewo).")

                # Handle errors
                if errors:
                    error_dialog = gui.Dlg(title="Błąd walidacji")
                    error_dialog.addText("Proszę poprawić następujące błędy:")
                    for error in errors:
                        error_dialog.addText(error)
                    error_dialog.show()
                    continue
                
                # Save values if they are correct
                self.age = int(raw_age)
                self.sex = clean_sex
                self.handedness = clean_hand
                break
            else:
                core.quit()
