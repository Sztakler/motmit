"""Definicje 24 bodźców i funkcje ich rysowania."""

import math
from psychopy import visual


def all_stimuli():
    """Zwraca 24 unikalne bodźce jako słowniki shape/color."""
    return [
        {"shape": shape, "color": color}
        for shape in ("koło", "kwadrat", "trójkąt", "romb", "krzyżyk", "gwiazdka")
        for color in ("czerwony", "żółty", "zielony", "niebieski")
    ]


def _vertices(shape):
    if shape == "kwadrat":
        return [(-1, -1), (1, -1), (1, 1), (-1, 1)]

    if shape == "trójkąt":
        return [
            (0, 1),
            (-math.sqrt(3) / 2, -0.5),
            (math.sqrt(3) / 2, -0.5),
        ]

    if shape == "romb":
        return [(0, 1), (0.78, 0), (0, -1), (-0.78, 0)]

    if shape == "krzyżyk":
        return [
            (-0.30, 1), (0.30, 1), (0.30, 0.30), (1, 0.30),
            (1, -0.30), (0.30, -0.30), (0.30, -1), (-0.30, -1),
            (-0.30, -0.30), (-1, -0.30), (-1, 0.30), (-0.30, 0.30),
        ]

    if shape == "gwiazdka":
        points = []
        for i in range(10):
            radius = 1.0 if i % 2 == 0 else 0.43
            angle = math.pi / 2 + i * math.pi / 5
            points.append((radius * math.cos(angle), radius * math.sin(angle)))
        return points

    raise ValueError(f"Nieznany kształt: {shape}")


def make_shape_stim(win, stimulus, pos, size):
    """Tworzy figurę, skalując jej dłuższy wymiar do `size` pikseli."""
    color = stimulus["color_hex"]
    shape = stimulus["shape"]

    if shape == "koło":
        return visual.Circle(
            win,
            radius=size / 2,
            pos=pos,
            fillColor=color,
            lineColor=color,
            units="pix",
        )

    vertices = _vertices(shape)
    xs = [point[0] for point in vertices]
    ys = [point[1] for point in vertices]
    max_dimension = max(max(xs) - min(xs), max(ys) - min(ys))

    # Normalizacja sprawia, że największy wymiar każdej figury
    # (szerokość lub wysokość) jest równy średnicy koła.
    normalized = [(x / max_dimension, y / max_dimension) for x, y in vertices]

    return visual.ShapeStim(
        win,
        vertices=normalized,
        pos=pos,
        size=(size, size),
        closeShape=True,
        fillColor=color,
        lineColor=color,
        lineWidth=1,
        units="pix",
    )
