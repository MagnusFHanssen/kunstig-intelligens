from my_enums import *
import random


class Qtable:
    def __init__(self, can_rest=False, dimensions=(10, 10)):
        self.table = {}
        self.alpha = 0.1
        self.alpha_decay = 0.99
        self.gamma = 0.7

        keys = [Actions.NORTH, Actions.SOUTH, Actions.WEST, Actions.EAST]
        if can_rest:
            keys.append(Actions.REST)
        for row in range(dimensions[0]):
            for col in range(dimensions[1]):
                self.table[(row, col)] = dict.fromkeys(keys, 0.0)

    def get_highest_q_value(self, state):
        return max(self.table[state].values())

    def get_highest_q_action(self, state):
        # return max(self.table[state], key=self.table[state].get)
        return random.choice(self.get_all_highest_q_actions(state))

    def get_all_highest_q_actions(self, state):
        return [action for action, q_value in self.table[state].items() if abs(q_value - max(self.table[state].values())) <= 0.0001]

    def update_alpha(self):
        self.alpha = self.alpha * self.alpha_decay

    def update_table(self, current_state, new_state, action, reward):
        q_current = self.table[current_state][action]

        q_max_next_state = self.get_highest_q_value(new_state if new_state is not None else current_state)
        new_q = (1 - self.alpha) * q_current + self.alpha * (q_max_next_state * self.gamma + reward)
        self.table[current_state][action] = new_q

    def cull_table(self, blocked_map):
        for key in blocked_map:
            self.table.pop(key, None)

    def decay_alpha(self):
        self.alpha = self.alpha_decay * self.alpha
