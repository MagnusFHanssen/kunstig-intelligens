import copy
import sys
import random
from qtable import Qtable

from my_enums import *


class Agent:
    def __init__(self, scenario, start_state, epsilon=0.8, epsilon_decay=0.99):
        self.scenario = scenario
        self.state = start_state
        self.start_state = start_state
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.q_table = Qtable()
        self.total_samples = 0

    def get_state(self):
        return self.state

    def set_state(self, state, deputy_state=None):
        self.state = state

    def reset_state(self):
        self.state = self.start_state

    def update(self, new_state, action, reward):
        old_state = self.state
        self.state = new_state
        self.total_samples += 1
        return self.q_table.update_table(old_state, new_state, action, reward)

    def cull_table(self, blocked_map):
        self.q_table.cull_table(blocked_map)

    def decay_epsilon(self):
        self.epsilon = self.epsilon * self.epsilon_decay

    def decay_alpha(self):
        self.q_table.decay_alpha()

    def get_best_move(self):
        return self.q_table.get_highest_q_action(self.state)


class BountyHunter(Agent):
    def __init__(self, scenario, start_state, model_based=False):
        super().__init__(scenario, start_state)
        self.model_based = model_based
        if model_based:
            self.r_table = None
            self.actions = None
            self.t_table = None
            self.v_table = None
            self.goal_state = None
            self.gamma = 0.7
            self.p_table = {}
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
            return self.get_move_d()

    def get_move_d(self):
        # TODO: Implement part D properly
        return None

    def get_best_move(self):
        if self.model_based:
            return self.get_move_p_i()
        else:
            return super(BountyHunter, self).get_best_move()

    def get_move_a(self):
        if self.model_based:
            return self.get_move_p_i()
        else:
            return self.get_move_a_q()

    def get_move_p_i(self):
        return self.p_table[self.state]

    def get_move_a_q(self):
        is_random = random.uniform(0, 1) < self.epsilon
        if not is_random:
            return self.q_table.get_highest_q_action(self.state)
        else:
            return random.choice([Actions.EAST, Actions.WEST, Actions.NORTH, Actions.SOUTH])

    def get_move_with_rest(self):
        is_random = random.uniform(0, 1) < self.epsilon
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

    def init_model_based(self, r_table, actions, t_table, goal_state):
        self.r_table = r_table
        self.actions = actions
        self.t_table = t_table
        self.goal_state = goal_state
        # Randomly select initial policy
        for state in t_table.keys():
            self.p_table[state] = random.choice(actions)

    def iterate_value(self):
        max_diff = 0
        if self.v_table:
            for state_0, adjacent_states in self.t_table.items():
                if state_0 == self.goal_state:
                    continue
                v_mark = self.r_table[state_0[0]][state_0[1]] \
                    + self.gamma * self.v_table[adjacent_states[self.p_table[state_0]]]
                self.total_samples += 1
                max_diff = max(max_diff, abs(v_mark - self.v_table[state_0]))
                self.v_table[state_0] = v_mark
        else:
            self.v_table = {}
            for state in self.t_table.keys():
                self.v_table[state] = self.r_table[state[0]][state[1]]
                self.total_samples += 1
            max_diff = max(max(self.v_table.values()), abs(min(self.v_table.values())))
        return max_diff

    def iterate_policy(self):
        for state_0, transitions in self.t_table.items():
            best_action = None
            best_value = - sys.maxsize
            for action, state_marked in transitions.items():
                if self.v_table[state_marked] > best_value:
                    best_action = action
                    best_value = self.v_table[state_marked]
            self.p_table[state_0] = best_action

    def print_policy(self):
        for x in range(10):
            row = ""
            for y in range(10):
                if (x, y) not in self.p_table.keys():
                    row += "■"
                else:
                    best_action = self.p_table[(x, y)]
                    if best_action is Actions.REST:
                        row += "R"
                    elif best_action is Actions.EAST:
                        row += "→"
                    elif best_action is Actions.WEST:
                        row += "←"
                    elif best_action is Actions.NORTH:
                        row += "↑"
                    else:
                        row += "↓"
            print(row)


class Bandit(Agent):
    def __init__(self, scenario, start_state):
        super().__init__(scenario, start_state)
        self.q_table = Qtable(True)

    def get_move(self):
        if self.scenario is Scenario.A or self.scenario is Scenario.B:
            return Actions.REST
        else:
            is_random = random.uniform(0, 1) < self.epsilon
            if not is_random:
                return self.q_table.get_highest_q_action(self.state)
            else:
                return random.choice([Actions.EAST, Actions.WEST, Actions.NORTH, Actions.SOUTH, Actions.REST])

    def get_state(self):
        if self.scenario is Scenario.B:
            self.hide_random()
        return self.state

    def hide_random(self):
        self.state = (5, 2) if random.randrange(1, 100) <= 35 else (3, 8)
    
    def update(self, new_state, action, reward):
        if self.scenario == Scenario.A:
            return 0
        elif self.scenario == Scenario.B:
            return 0
        else:
            return super(Bandit, self).update(new_state, action, reward)


