from enum import IntEnum, Enum, auto

class Side(IntEnum):
    LEFT = 0
    RIGHT = 1

class OrbitPosition(IntEnum):
    TOP = 0
    MIDDLE = 1
    BOTTOM = 2

class TrialType(Enum):
    MOT = auto()
    MIT = auto()

class Layout(Enum):
    # Positions and weight (for balancing)
    ALL = ((OrbitPosition.TOP, OrbitPosition.MIDDLE, OrbitPosition.BOTTOM), 3)
    TOP_MID = ((OrbitPosition.TOP, OrbitPosition.MIDDLE), 1)
    MID_BOT = ((OrbitPosition.MIDDLE, OrbitPosition.BOTTOM), 1)
    TOP_BOT = ((OrbitPosition.TOP, OrbitPosition.BOTTOM), 1)
