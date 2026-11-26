"""Konfiguracja pilotażu bodźców."""

WINDOW_SIZE = (1920, 1080)
FULLSCREEN = True

# Czas prezentacji orbitujących bodźców.
ORBIT_DURATION = 5.0
FIXATION_DURATION = 0.5
INTER_TRIAL_INTERVAL = 0.35

# 1 oznacza jedną prezentację każdej z 276 par.
REPEATS = 5
BREAK_EVERY = 48

ORBIT_RADIUS = 95
STIMULUS_SIZE = 62
ORBIT_CENTERS_X = (-510, 510)
ORBIT_CENTER_Y = 0

# Prędkość kątowa w radianach na sekundę.
ORBIT_SPEED = 2.0

# PsychoPy colorSpace="rgb": wartości od -1 (ciemny) do 1 (jasny).
BACKGROUND_COLOR = (0.5, 0.5, 0.5)
TEXT_COLOR = "black"

SHAPES = ("koło", "kwadrat", "trójkąt", "romb", "krzyżyk", "gwiazdka")
COLORS = {
    "czerwony": "#e53935",
    "żółty": "#fdd835",
    "zielony": "#43a047",
    "niebieski": "#1e88e5",
}
