import copy
import random
import time

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

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
    export_result = True

    def __init__(self, scenario, episodes=10000):
        self.scenario = scenario
        self.episodes = episodes
        self.bounty_hunter = None
        self.bandit = None
        self.renderer = None
        self.current_episode = 1
        self.convergent = False
        self.q_change_list: list[float] = []
        self.v_change_list: list[float] = []
        self.loot_locations = {(4, 6), (0, 9), (9, 4), (5, 2)}
        self.loot_state = random.choice([loc for loc in self.loot_locations])
        self.bh_reward_list = []
        self.bandit_reward_list = []

        self.t_table = {}
        for row in range(self.height):
            for col in range(self.width):
                state = (row, col)
                if state not in self.blocked_map:
                    self.t_table[state] = {}

        actions = [Actions.EAST, Actions.WEST, Actions.NORTH, Actions.SOUTH, Actions.REST] if scenario != Scenario.A \
            else [Actions.EAST, Actions.WEST, Actions.NORTH, Actions.SOUTH]
        for state_0 in self.t_table.keys():
            for action in actions:
                state_1 = self.test_move(state_0, action)
                self.t_table[state_0][action] = state_1 if state_1 else state_0

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
        penalty = self.r_map[state[0]][state[1]] + (self.wait_cost if action is Actions.REST else self.move_cost)
        if is_bounty_hunter:
            bandit_state = self.bandit.get_state()
            return penalty + (1000 if state == bandit_state or bandit_state in state else 0)
        elif state == self.loot_state:
            self.loot_state = random.choice([loc for loc in self.loot_locations if loc != self.loot_state])
            return penalty + 1000
        else:
            return penalty


    def get_random_state(self):
        state = None
        while state is None or state in self.blocked_map:
            state = (random.randint(0, 9), random.randint(0, 9))
        return state

    def is_caught(self):
        bandit_state = self.bandit.state
        return self.bounty_hunter.get_state() == bandit_state or self.bounty_hunter.deputy_state == bandit_state

    def train(self):
        if self.bounty_hunter.model_based:
            self.train_p_i()
        else:
            self.train_q()

    def train_p_i(self):
        actions = [Actions.EAST, Actions.WEST, Actions.NORTH, Actions.SOUTH]
        r_table = copy.deepcopy(self.r_map)
        r_table[self.bandit.get_state()[0]][self.bandit.get_state()[1]] = 1000
        r_table[:] = [r + self.move_cost for r in r_table]

        self.bounty_hunter.init_model_based(r_table, actions, self.t_table, self.bandit.get_state())

        while self.current_episode < self.episodes and not self.convergent:
            self.v_change_list.append(self.bounty_hunter.iterate_value())
            self.bounty_hunter.iterate_policy()
            if max(self.v_change_list[-10:]) < 1:
                self.convergent = True
            else:
                self.current_episode += 1

    def train_q(self):
        self.bounty_hunter.cull_table(self.blocked_map)
        self.bandit.cull_table(self.blocked_map)

        max_change = 0
        while self.current_episode < self.episodes and not self.convergent:
            bounty_hunter_start = self.get_random_state()
            self.bounty_hunter.set_state(bounty_hunter_start,
                                         bounty_hunter_start if self.bounty_hunter.deputy_state is not None else None)
            self.bandit.reset_state()
            if self.scenario in [Scenario.C, Scenario.D]:
                self.bandit.set_state(self.get_random_state())
            # Episode:
            move_count = 0
            bandit_reward = 0
            bounty_hunter_reward = 0
            while move_count < self.max_moves:
                bh_move = self.bounty_hunter.get_move()
                bh_new_state = self.test_move(self.bounty_hunter.get_state(), bh_move)
                if bh_new_state is None:
                    bh_new_state = self.bounty_hunter.get_state()
                reward = self.get_reward(bh_new_state, bh_move)
                max_change = max(max_change, self.bounty_hunter.update(bh_new_state, bh_move, reward))
                bounty_hunter_reward += reward
                if self.is_caught():
                    break

                bandit_move = self.bandit.get_move()
                bandit_new_state = self.test_move(self.bandit.get_state(), bandit_move)
                if bandit_new_state is None:
                    bandit_new_state = self.bandit.get_state()
                reward = self.get_reward(bandit_new_state, bandit_move, False)
                max_change = max(max_change, self.bandit.update(bandit_new_state, bandit_move, reward))
                bandit_reward += reward
                move_count += 1

            self.bh_reward_list.append(bounty_hunter_reward)
            self.bandit_reward_list.append(bandit_reward)

            self.q_change_list.append(max_change)
            max_change = 0
            if max(self.q_change_list[-10:]) < 1:
                self.convergent = True
            else:
                self.current_episode += 1
                self.__decay(self.bounty_hunter, 20, 40)
                self.__decay(self.bandit, 20, 40)

    def render(self, renderer):
        if renderer.running:
            renderer.update(self.bounty_hunter.get_state(), self.bandit.state, self.bounty_hunter.deputy_state)

    def __decay(self, agent, alpha_count, epsilon_count):
        if self.current_episode % epsilon_count == 0:
            agent.decay_epsilon()
        if self.current_episode % alpha_count == 0:
            agent.decay_alpha()

    def show_solution(self):
        from renderer import Renderer
        self.bounty_hunter.reset_state()
        self.bandit.reset_state()
        if self.scenario == Scenario.C or self.scenario == Scenario.D:
            r = Renderer(self.loot_locations)
        else:
            r = Renderer()
        self.render(r)
        while r.running:
            bh_move = self.bounty_hunter.get_best_move()
            bh_new_state = self.test_move(self.bounty_hunter.get_state(), bh_move)
            if bh_new_state is None:
                bh_new_state = self.bounty_hunter.get_state()

            self.bounty_hunter.set_state(bh_new_state)
            if self.is_caught():
                self.render(r)
                time.sleep(2)
                r.quit()
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
        if self.export_result:
            plt.savefig('results/scenario_{}_q_learning.png'.format(self.scenario.name), bbox_inches='tight')
        plt.show()

    def plot_max_v_change(self):
        plt.plot(self.v_change_list)
        plt.title("Scenario {}: Policy Iteration: Max change in V(s)".format(self.scenario.name))
        plt.xlabel("Episode")
        plt.ylabel("Max difference")
        axes = plt.gca()
        min_x, max_x = axes.get_xlim()
        min_y, max_y = axes.get_ylim()
        gamma_str = "\u03B3"
        plt.text(max_x - max_x * 0.35, max_y - max_y * 0.15,
                 f'Decay {gamma_str}: {round(self.bounty_hunter.gamma, 3)}\nNo. Episodes: '
                 f'{self.current_episode}', bbox=dict(facecolor='grey', alpha=0.5))
        if self.export_result:
            plt.savefig('results/scenario_{}_pol_iteration.png'.format(self.scenario.name), bbox_inches='tight')
        plt.show()

    def plot_rewards_over_time(self, rolling_average=True):
        df = pd.DataFrame({'Bounty Hunter': self.bh_reward_list, 'Bandit': self.bandit_reward_list})
        df['Rolling BH'] = df['Bounty Hunter'].rolling(100).mean()
        if self.scenario in [Scenario.C, Scenario.D]:
            df['Rolling Bandit'] = df['Bandit'].rolling(100).mean()
        if rolling_average:
            plt.plot(df['Rolling BH'], label='Bounty Hunter')
            if self.scenario in [Scenario.C, Scenario.D]:
                plt.plot(df['Rolling Bandit'], label='Bandit')
            plt.title('Rolling average of the rewards per episode of scenario {}'.format(self.scenario.name))
        else:
            plt.plot(df['Bounty Hunter'], label='Bounty Hunter')
            if self.scenario in [Scenario.C, Scenario.D]:
                plt.plot(df['Bandit'], label='Bandit')
            plt.title('Rewards per episode of scenario {}'.format(self.scenario.name))
        plt.xlabel("Episode")
        plt.ylabel("Reward")
        plt.legend(loc='lower left')
        if self.export_result:
            plt.savefig('results/scenario_{}_reward.png'.format(self.scenario.name), bbox_inches='tight')
        plt.show()
