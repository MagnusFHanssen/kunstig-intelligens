from enum import Enum


class Scenario(Enum):
    A = 0
    B = 1
    C = 2
    D = 3


class Actions(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3
    REST = 4
