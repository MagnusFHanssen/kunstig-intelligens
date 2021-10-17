from world import *

class Agent:
    def __init__(self, scenario, start_pos):
        self.scenario = scenario
        self.position = start_pos


class BountyHunter(Agent):
    def __init__(self, scenario, start_pos, model_based=False):
        super().__init__(scenario, start_pos)
        self.model_based = model_based


class Bandit(Agent):
    def __init__(self, scenario, start_pos):
        super().__init__(scenario, start_pos)

