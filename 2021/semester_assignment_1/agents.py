import sys
import random
from qtable import Qtable

from my_enums import *


class Agent:
    def __init__(self, scenario, start_state, epsilon=0.9, epsilon_decay=0.9):
        self.scenario = scenario
        self.state = start_state
        self.start_state = start_state
        self.change = sys.maxsize
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.q_table = Qtable()

    def get_state(self):
        return self.state

    def set_state(self, state, deputy_state=None):
        self.state = state

    def reset_state(self):
        self.state = self.start_state

    def update(self, new_state, action, reward):
        old_state = self.state
        self.state = new_state
        self.q_table.update_table(old_state, new_state, action, reward)

    def cull_table(self, blocked_map):
        self.q_table.cull_table(blocked_map)

    def decay_epsilon(self):
        self.epsilon = self.epsilon * self.epsilon_decay

    def decay_alpha(self):
        self.q_table.decay_alpha()


class BountyHunter(Agent):
    def __init__(self, scenario, start_state, model_based=False):
        super().__init__(scenario, start_state)
        self.model_based = model_based
        if self.scenario == Scenario.D:
            self.deputy_state = start_state
        else:
            self.deputy_state = None
        if scenario is not Scenario.A:
            self.q_table = Qtable(True)

    def get_move(self):
        if self.scenario is Scenario.A:
            return self.get_move_a()
        elif self.scenario is not Scenario.D:
            return self.get_move_with_rest()
        else:
            return None

    def get_move_a(self):
        is_random = random.uniform(0, 1) <= self.epsilon
        if not is_random:
            return self.q_table.get_highest_q_action(self.state)
        else:
            return random.choice([Actions.EAST, Actions.WEST, Actions.NORTH, Actions.SOUTH])

    def get_move_with_rest(self):
        is_random = random.uniform(0, 1) <= self.epsilon
        if not is_random:
            return self.q_table.get_highest_q_action(self.state)
        else:
            return random.choice([Actions.EAST, Actions.WEST, Actions.NORTH, Actions.SOUTH, Actions.REST])

    def set_state(self, state, deputy_state=None):
        self.state = state
        self.deputy_state = deputy_state

    def reset_state(self):
        self.state = self.start_state
        if self.deputy_state is not None:
            self.deputy_state = self.start_state


class Bandit(Agent):
    def __init__(self, scenario, start_state):
        super().__init__(scenario, start_state)
        self.q_table = Qtable(True)

    def get_move(self):
        if self.scenario is Scenario.A or self.scenario is Scenario.B:
            return Actions.REST
        else:
            return None

    def get_state(self):
        if self.scenario is Scenario.B:
            self.hide_random()
        return self.state

    def hide_random(self):
        self.state = (5, 2) if random.randrange(1, 100) <= 35 else (3, 9)
    
    def update(self, new_state, action, reward):
        if self.scenario == Scenario.A:
            return None
        elif self.scenario == Scenario.B:
            return None
        else:
            super(Bandit, self).update(new_state, action, reward)


