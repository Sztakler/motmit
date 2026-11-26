import csv
import math
import random
import time
from itertools import combinations
from pathlib import Path

from psychopy import visual, core, event, gui

from config import (
    WINDOW_SIZE, FULLSCREEN, ORBIT_DURATION, FIXATION_DURATION,
    INTER_TRIAL_INTERVAL, REPEATS, BREAK_EVERY, ORBIT_RADIUS,
    STIMULUS_SIZE, ORBIT_CENTERS_X, ORBIT_CENTER_Y, ORBIT_SPEED,
    BACKGROUND_COLOR, TEXT_COLOR, COLORS,
)
from stimuli import all_stimuli, make_shape_stim


def stimulus_key(stim):
    return (stim["shape"], stim["color"])


def pair_category(a, b):
    same_shape = a["shape"] == b["shape"]
    same_color = a["color"] == b["color"]
    if same_shape:
        return "ten_sam_ksztalt"
    if same_color:
        return "ten_sam_kolor"
    return "rozny_ksztalt_i_kolor"


def generate_trials():
    """Generuje wszystkie 276 nieuporządkowanych par różnych bodźców."""
    stimuli = all_stimuli()
    pairs = list(combinations(stimuli, 2))
    trials = []

    for repeat_index in range(REPEATS):
        repetition = [
            {
                "stimulus_a": dict(a),
                "stimulus_b": dict(b),
                "repeat": repeat_index + 1,
            }
            for a, b in pairs
        ]
        random.shuffle(repetition)
        trials.extend(repetition)

    return trials


class Pilot:
    def __init__(self, win, participant_id):
        self.win = win
        self.participant_id = participant_id
        self.mouse = event.Mouse(win=win)
        self.fixation = visual.TextStim(
            win, text="+", height=42, color=TEXT_COLOR, units="pix"
        )

    def draw_text(self, text, pos=(0, 0), height=28, color=TEXT_COLOR):
        visual.TextStim(
            self.win, text=text, pos=pos, height=height,
            color=color, wrapWidth=1200, units="pix"
        ).draw()

    def check_escape(self):
        if "escape" in event.getKeys():
            core.quit()

    def wait_for_mouse_release(self):
        while any(self.mouse.getPressed()):
            self.check_escape()
            self.win.flip()

    def wait_for_click(self, draw_callback):
        """Czeka na kliknięcie; Escape kończy program."""
        self.wait_for_mouse_release()
        while True:
            self.check_escape()
            draw_callback()

            if self.mouse.getPressed()[0]:
                pos = self.mouse.getPos()
                self.wait_for_mouse_release()
                return pos
            self.win.flip()

    def show_instructions(self):
        lines = (
            "Zobaczysz parę obiektów poruszających się po orbitach.",
            "Twoim zadaniem jest ocenić, czy potrafiłeś rozróżnić oba obiekty.",
            "Po każdej prezentacji wybierz jedną z dwóch odpowiedzi:",
            "„Rozróżniałem” albo „Nie rozróżniałem”.",
            "",
            "Nie ma limitu czasu na odpowiedź.",
            "",
            "Kliknij, aby rozpocząć.",
        )

        def draw():
            self.draw_text("\n".join(lines), height=27)

        self.win.flip()
        self.wait_for_click(draw)

    def show_fixation(self, duration=FIXATION_DURATION):
        clock = core.Clock()
        while clock.getTime() < duration:
            self.fixation.draw()
            self.win.flip()
            self.check_escape()

    def show_orbits(self, stimulus_a, stimulus_b):
        """Rysuje lustrzane orbity; punkt fiksacji na środku."""
        angle0 = random.uniform(0, 2 * math.pi)
        direction = random.choice((-1, 1))
        clock = core.Clock()

        a = dict(stimulus_a, color_hex=COLORS[stimulus_a["color"]])
        b = dict(stimulus_b, color_hex=COLORS[stimulus_b["color"]])

        while clock.getTime() < ORBIT_DURATION:
            t = clock.getTime()
            angle = angle0 + direction * ORBIT_SPEED * t

            left_center = ORBIT_CENTERS_X[0]
            left_a_pos = (
                left_center + ORBIT_RADIUS * math.cos(angle),
                ORBIT_CENTER_Y + ORBIT_RADIUS * math.sin(angle),
            )
            left_b_pos = (
                left_center + ORBIT_RADIUS * math.cos(angle + math.pi),
                ORBIT_CENTER_Y + ORBIT_RADIUS * math.sin(angle + math.pi),
            )

            right_center = ORBIT_CENTERS_X[1]
            right_angle = math.pi - angle
            right_a_pos = (
                right_center + ORBIT_RADIUS * math.cos(right_angle),
                ORBIT_CENTER_Y + ORBIT_RADIUS * math.sin(right_angle),
            )
            right_b_pos = (
                right_center + ORBIT_RADIUS * math.cos(right_angle + math.pi),
                ORBIT_CENTER_Y + ORBIT_RADIUS * math.sin(right_angle + math.pi),
            )

            for stim, pos in (
                (a, left_a_pos), (b, left_b_pos),
                (a, right_a_pos), (b, right_b_pos),
            ):
                make_shape_stim(
                    self.win, stim, pos=pos, size=STIMULUS_SIZE
                ).draw()

            self.fixation.draw()
            self.win.flip()
            self.check_escape()

    def response_screen(self):
        button_width, button_height = 390, 125
        button_y = -40
        buttons = [
            (
                "rozroznialem",
                visual.Rect(
                    self.win, width=button_width, height=button_height,
                    pos=(-220, button_y), fillColor="#d9ead3",
                    lineColor="#38761d", lineWidth=2, units="pix",
                ),
                visual.TextStim(
                    self.win, text="Rozróżniałem", pos=(-220, button_y),
                    height=30, color="black", units="pix",
                ),
            ),
            (
                "nie_rozroznialem",
                visual.Rect(
                    self.win, width=button_width, height=button_height,
                    pos=(220, button_y), fillColor="#f4cccc",
                    lineColor="#990000", lineWidth=2, units="pix",
                ),
                visual.TextStim(
                    self.win, text="Nie rozróżniałem", pos=(220, button_y),
                    height=30, color="black", units="pix",
                ),
            ),
        ]

        response_clock = core.Clock()
        response_clock.reset()

        while True:
            self.draw_text(
                "Czy potrafiłeś rozróżnić dwa prezentowane obiekty?",
                pos=(0, 170), height=30,
            )
            for _value, rect, label in buttons:
                rect.draw()
                label.draw()
            self.win.flip()

            self.check_escape()
            if self.mouse.getPressed()[0]:
                pos = self.mouse.getPos()
                self.wait_for_mouse_release()
                for value, rect, _label in buttons:
                    if rect.contains(pos):
                        return value, response_clock.getTime()

    def run_trial(self, trial, trial_number, total_trials):
        self.show_fixation()
        self.show_orbits(trial["stimulus_a"], trial["stimulus_b"])

        # Ekran odpowiedzi nie zawiera krzyża fiksacyjnego.
        self.win.flip()
        response, response_time = self.response_screen()

        a = trial["stimulus_a"]
        b = trial["stimulus_b"]
        return {
            "participant_id": self.participant_id,
            "trial_number": trial_number,
            "total_trials": total_trials,
            "repeat": trial["repeat"],
            "stimulus_a_shape": a["shape"],
            "stimulus_a_color": a["color"],
            "stimulus_b_shape": b["shape"],
            "stimulus_b_color": b["color"],
            "pair_category": pair_category(a, b),
            "discriminated": int(response == "rozroznialem"),
            "response": response,
            "response_time_seconds": round(response_time, 4),
        }

    def show_break(self, completed, total):
        def draw():
            self.draw_text(
                f"Przerwa\n\nWykonano {completed} z {total} prób.\n\n"
                "Kliknij, aby kontynuować.",
                height=30,
            )

        self.win.flip()
        self.wait_for_click(draw)

    def show_end(self, output_file):
        def draw():
            self.draw_text(
                "Koniec badania. Dziękujemy za udział!\n\n"
                f"Wyniki zapisano w:\n{output_file}",
                height=26,
            )

        self.win.flip()
        self.wait_for_click(draw)


def run():
    participant = {"participant_id": ""}
    dialog = gui.DlgFromDict(
        participant,
        title="Pilotaż rozpoznawania bodźców",
        order=["participant_id"],
    )
    if not dialog.OK:
        core.quit()

    participant_id = participant["participant_id"].strip() or "anonymous"

    output_dir = Path("data")
    output_dir.mkdir(exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"{participant_id}_{timestamp}.csv"

    win = visual.Window(
        size=WINDOW_SIZE,
        fullscr=FULLSCREEN,
        units="pix",
        color=BACKGROUND_COLOR,
        colorSpace="rgb",
    )

    pilot = Pilot(win, participant_id)
    trials = generate_trials()

    fieldnames = [
        "participant_id", "trial_number", "total_trials", "repeat",
        "stimulus_a_shape", "stimulus_a_color",
        "stimulus_b_shape", "stimulus_b_color",
        "pair_category", "discriminated", "response",
        "response_time_seconds",
    ]

    try:
        pilot.show_instructions()
        with output_file.open("w", newline="", encoding="utf-8-sig") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            for index, trial in enumerate(trials, start=1):
                row = pilot.run_trial(trial, index, len(trials))
                writer.writerow(row)
                csv_file.flush()

                if index < len(trials) and index % BREAK_EVERY == 0:
                    pilot.show_break(index, len(trials))

                if index < len(trials):
                    # Krzyż fiksacyjny jest widoczny także w przerwie między próbami.
                    pilot.show_fixation(INTER_TRIAL_INTERVAL)

        pilot.show_end(output_file)

    finally:
        win.close()
        core.quit()


if __name__ == "__main__":
    run()
