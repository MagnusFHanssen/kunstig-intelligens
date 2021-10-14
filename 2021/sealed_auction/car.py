from enum import Enum
from random import randrange


class Strategy(Enum):
    RANDOM = 1
    STATIC = 2
    SMART = 3


class Car:
    def __init__(self, budget, reward, cost, stalemate, strategy=Strategy.RANDOM):
        self.budget = budget
        self.reward = reward
        self.cost = cost
        self.stalemate = stalemate
        self.strategy = strategy

    def bid(self):
        if self.strategy is Strategy.RANDOM:
            return randrange(0, 2*self.cost+1)
        elif self.strategy is Strategy.STATIC:
            return max(self.reward-1, self.cost-1)
        elif self.strategy is Strategy.SMART:
            # TODO: Implement a "smart" strategy
            return 0

    def win(self, bid):
        self.budget += self.reward - bid

    def loss(self, bid):
        self.budget += bid - self.cost

    def draw(self):
        self.budget -= self.stalemate
