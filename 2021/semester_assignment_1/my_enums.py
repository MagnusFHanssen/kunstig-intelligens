from enum import Enum


class Scenario(Enum):
    A = 0
    B = 1
    C = 2
    D = 3


class Actions(Enum):
    NORTH = (-1, 0)
    EAST = (0, 1)
    SOUTH = (1, 0)
    WEST = (0, -1)
    REST = (0, 0)
