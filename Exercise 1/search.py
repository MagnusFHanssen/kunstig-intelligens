import random as rnd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors


class MapNode:
    def __init__(self, x, y, gcost, goal):
        self.gCost = gcost
        self.hCost = abs(x - goal[0]) + abs(y - goal[1])
        self.x = x
        self.y = y
        self.fCost = self.gCost + self.hCost

    def __eq__(self, other):
        return self.fCost == other.fCost

    def __lt__(self, other):
        return self.fCost < other.fCost


class SearchMap:
    cmap = colors.ListedColormap(['white', 'green', 'red', 'yellow', 'purple'])
    path = []

    def __init__(self, width=10, height=10):
        self.height = height
        self.width = width
        self.map = np.ones((self.height, self.height))
        self.start = [rnd.randint(0, self.height / 2 - 1), rnd.randint(0, self.width / 2 - 1)]
        self.goal = [rnd.randint(self.height / 2, self.height - 1), rnd.randint(self.width / 2, self.width - 1)]

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
        self.map[self.start[1]][self.start[0]] = 4
        self.map[self.goal[1]][self.goal[0]] = 5

    def plot_chart(self):
        plt.figure(figsize=(6, 6))
        plt.pcolor(searchMap.map, cmap=self.cmap, edgecolors='k', linewidths=3)
        plt.show()

    def h(self, x, y):
        return abs(x - self.goal[0]) + abs(y - self.goal[1])

    def plot(self, x, y):
        plt.scatter([x + 0.5], [y + 0.5], s=(1200 / max(self.width, self.height)))

    def get_neighbours(self, x, y):
        list = []
        # Node to the left
        if x >= 1:
            list.append(MapNode(x - 1, y, ))

searchMap = SearchMap()


exit(0)
