import numpy as np
from enum import Enum
from agents import BountyHunter, Bandit
import PySimpleGUI as sg


class Scenario(Enum):
    A = 0
    B = 1
    C = 2
    D = 3


class World:
    height = 10
    width = 10
    r_map = np.zeros((height, width))
    r_map[4][4] = -100
    r_map[0][8] = -500
    t_map = np.zeros((10, 10))
    blocked_map = {(3, 1), (3, 2), (3, 7), (4, 1), (4, 2), (4, 7), (5, 6),
                   (5, 7), (6, 6), (6, 7)}

    def __init__(self, scenario):
        self.scenario = scenario
