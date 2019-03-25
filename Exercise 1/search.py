import random as rnd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors


class MapNode:
    def __init__(self, x, y, gCost, hCost):
        self.gCost = gCost
        self.hCost = hCost
        self.x = x
        self.y = y
        self.fCost = self.gCost + self.hCost

    def __eq__(self, other):
        return self.fCost == other.fCost

    def __lt__(self, other):
        return self.fCost < other.fCost


class SearchMap:
    cmap = colors.ListedColormap(['white', 'green', 'red', 'yellow', 'purple'])
    height = 10
    width = 10

    def __init__(self):
        self.map = np.ones((self.height, self.height))
        self.start = [rnd.randint(0, self.height/2 - 1), rnd.randint(0, self.width/2 - 1)]
        self.goal = [rnd.randint(self.height/2, self.height - 1), rnd.randint(self.width/2, self.width - 1)]

        while self.start == self.goal:
            self.goal = [rnd.randint(0, self.height - 1), rnd.randint(0, self.width - 1)]

        for y in range(0, self.height - 1):
            for x in range(0, self.width - 1):
                r = rnd.random()
                if r < 0.1:
                    self.map[y][x] = 3
                else:
                    if r > 0.8:
                        self.map[y][x] = 2
        self.map[self.start[0]][self.start[1]] = 4
        self.map[self.goal[0]][self.goal[1]] = 5

    def plot(self):
        plt.figure(figsize=(6, 6))
        plt.xticks(np.arange(0.5, 10.5, step=1))
        plt.yticks(np.arange(0.5, 10.5, step=1))
        plt.pcolor(searchMap.map, cmap=self.cmap, edgecolors='k', linewidths=3)

    def path(self):
        return [1, 2]





searchMap = SearchMap()




