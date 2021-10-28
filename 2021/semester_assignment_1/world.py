import random
import time

import numpy as np
import matplotlib.pyplot as plt

from agents import BountyHunter, Bandit
from my_enums import *


class World:
    height = 10
    width = 10
    move_cost = -5
    wait_cost = -5
    r_map = np.zeros((height, width))
    r_map[4][4] = -100
    r_map[0][8] = -500
    t_map = np.zeros((10, 10))
    blocked_map = {(3, 1), (3, 2), (3, 7), (4, 1), (4, 2), (4, 7), (5, 6),
                   (5, 7), (6, 6), (6, 7)}
    max_moves = 10000

    def __init__(self, scenario, episodes=10000):
        self.scenario = scenario
        self.episodes = episodes
        self.bounty_hunter = None
        self.bandit = None
        self.renderer = None
        self.current_episode = 1
        self.convergent = False
        self.q_change_list: list[float] = []

    def set_agent(self, agent):
        if isinstance(agent, BountyHunter):
            self.bounty_hunter = agent
        elif isinstance(agent, Bandit):
            self.bandit = agent

    def test_move(self, state, action: Actions):
        if action == Actions.REST:
            return state
        else:
            new_state = (state[0] + action.value[0], state[1] + action.value[1])
            if max(new_state) < 10 and min(new_state) >= 0 and new_state not in self.blocked_map:
                return new_state
            else:
                return None

    def get_reward(self, state, action, is_bounty_hunter=True):
        bandit_state = self.bandit.get_state()
        penalty = self.r_map[state[0]][state[1]] + (self.wait_cost if action is Actions.REST else self.move_cost)
        return penalty + (1000 if state == bandit_state and is_bounty_hunter else 0)

    def get_random_state(self):
        state = None
        while state is None or state in self.blocked_map:
            state = (random.randint(0, 9), random.randint(0, 9))
        return state

    def is_caught(self):
        bandit_state = self.bandit.state
        return self.bounty_hunter.get_state() == bandit_state or self.bounty_hunter.deputy_state == bandit_state

    def train(self):
        self.bounty_hunter.cull_table(self.blocked_map)
        self.bandit.cull_table(self.blocked_map)

        max_change = 0
        while self.current_episode <= self.episodes and not self.convergent:
            bounty_hunter_start = self.get_random_state()
            self.bounty_hunter.set_state(bounty_hunter_start,
                                         bounty_hunter_start if self.bounty_hunter.deputy_state is not None else None)
            self.bandit.reset_state()
            # Episode:
            move_count = 0
            while move_count < self.max_moves:
                bh_move = self.bounty_hunter.get_move()
                bh_new_state = self.test_move(self.bounty_hunter.get_state(), bh_move)
                if bh_new_state is None:
                    bh_new_state = self.bounty_hunter.get_state()

                max_change = max(max_change, self.bounty_hunter.update(bh_new_state, bh_move,
                                                                       self.get_reward(bh_new_state, bh_move)))
                if self.is_caught():
                    break

                bandit_move = self.bandit.get_move()
                bandit_new_state = self.test_move(self.bandit.get_state(), bandit_move)
                max_change = max(max_change, self.bandit.update(bandit_new_state, bandit_move,
                                                                self.get_reward(bandit_new_state, bandit_move, False)))
                move_count += 1
            self.q_change_list.append(max_change)
            max_change = 0
            if max(self.q_change_list[-10:]) < 1:
                self.convergent = True
            else:
                self.current_episode += 1
                self.__decay(self.bounty_hunter, 20, 40)
                self.__decay(self.bandit, 20, 40)

    def render(self, renderer):
        renderer.update(self.bounty_hunter.get_state(), self.bandit.state, self.bounty_hunter.deputy_state)

    def __decay(self, agent, alpha_count, epsilon_count):
        if self.current_episode % epsilon_count == 0:
            agent.decay_epsilon()
        if self.current_episode % alpha_count == 0:
            agent.decay_alpha()

    def show_solution(self):
        from renderer import Renderer
        self.bounty_hunter.reset_state()
        r = Renderer()
        self.render(r)
        while True:
            bh_move = self.bounty_hunter.get_best_move()
            bh_new_state = self.test_move(self.bounty_hunter.get_state(), bh_move)
            if bh_new_state is None:
                bh_new_state = self.bounty_hunter.get_state()

            self.bounty_hunter.set_state(bh_new_state)
            if self.is_caught():
                self.render(r)
                time.sleep(2)
                break

            if self.scenario is Scenario.C or self.scenario is Scenario.D:
                bandit_move = self.bandit.get_best_move()
                bandit_new_state = self.test_move(self.bandit.get_state(), bandit_move)
                if bandit_new_state is None:
                    bandit_new_state = self.bandit.get_state()
            else:
                bandit_new_state = self.bandit.get_state()
            self.bandit.set_state(bandit_new_state)
            self.render(r)

        r.quit()

    def plot_max_q_change(self):
        plt.plot(self.q_change_list)
        plt.title("Scenario {}: Q-learning: Max change in Q-values".format(self.scenario.name))
        plt.xlabel("Episode")
        plt.ylabel("Max difference")
        axes = plt.gca()
        min_x, max_x = axes.get_xlim()
        min_y, max_y = axes.get_ylim()
        alpha_str = "\u03B1"
        eps_str = "\u03B5"
        plt.text(max_x - max_x * 0.35, max_y - max_y * 0.15,
                 f'Last {eps_str}: {round(self.bounty_hunter.epsilon, 3)}\nLast {alpha_str}: '
                 f'{round(self.bounty_hunter.q_table.alpha, 3)}\nNo. Episodes: '
                 f'{self.current_episode}', bbox=dict(facecolor='grey', alpha=0.5))
        plt.show()
