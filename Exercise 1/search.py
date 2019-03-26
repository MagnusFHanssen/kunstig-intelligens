import random as rnd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors


def heuristic(x1, y1, x2, y2):
    """
    This heuristic makes the assumption that it's possible
    to reach the goal by the ideal route from any node.
    The length of a theoretical ideal path can then be found.
    Thus, if the ideal path through any node is longer than
    the shortest path already found, that path can be discarded.
    :param x1: x-coordinate of first node
    :param y1: y-coordinate of first node
    :param x2: x-coordinate of second node
    :param y2: y-coordinate of second note
    :return: the smallest possible distance between nodes
    """
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    return int(max(dx, dy))


class MapNode:
    def __init__(self, x, y, cost, goal, parent=None):
        self.cost = cost
        self.gcost = cost + (parent.gcost if parent is not None else 0)
        self.hcost = heuristic(x, y, goal[0], goal[1])
        self.x = x
        self.y = y
        self.fcost = self.gcost + self.hcost
        self.parent = parent

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y  # self.fcost == other.fcost

    def __lt__(self, other):
        return self.fcost < other.fcost

    def same(self, node):
        return self.x == node.x and self.y == node.y if node is not None else False

    def set_parent(self, node):
        self.parent = node
        gcost = self.cost + self.parent.gcost


class World:
    cmap = colors.ListedColormap(['purple', 'white', 'green', 'red', 'yellow'])
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
                elif r > 0.8:
                    self.map[y][x] = 2
        self.map[self.start[1]][self.start[0]] = 4
        self.map[self.goal[1]][self.goal[0]] = 0

    def plot_chart(self, tracks=[]):
        plt.figure(figsize=(6, 6))
        plt.pcolor(world.map, cmap=self.cmap, edgecolors='k', linewidths=3)
        for track in tracks:
            self.plot(track[0], track[1])
        plt.show()

    def plot(self, x, y):
        plt.scatter([x + 0.5], [y + 0.5], s=(1200 / max(self.width, self.height)), c='blue')

    def get_children(self, node):
        nodes = []
        for x in range(node.x - 1 if node.x != 0 else 0, node.x + 2 if node.x != self.width - 1 else node.x + 1):
            for y in range(node.y - 1 if node.y != 0 else 0, node.y + 2 if node.y != self.height - 1 else node.y + 1):
                if (x != node.x) or (y != node.y):
                    nodes.append(MapNode(x, y, self.map[y][x], self.goal, node))
        return nodes

    def backtrack(self, node):
        tracks = list()
        current = node
        count = 0
        while current.parent is not None and count < 1000 and (current != node or count == 0):
            tracks.append([current.x, current.y])
            current = current.parent
            count += 1

        return tracks

    def find_best_route(self):
        startnode = MapNode(self.start[0], self.start[1], 0, self.goal)
        goalnode = MapNode(self.goal[0], self.goal[1], 0, self.goal)

        h = list()
        s = list()
        fmax = 5 * self.width * self.height

        s.append(startnode)
        success = stop = False
        cycles = 0
        current = None

        while not (stop or success):
            if len(s) == 0:
                stop = True
                break
            s.sort(reverse=True)
            current = s.pop()
            if goalnode.same(current):
                success = True
                break
            children = self.get_children(current)
            h.append(current)
            for node in children:
                cycles += 1
                if not h.count(node) and node.gcost < fmax:
                    if s.count(node):
                        if s[s.index(node)].gcost > node.gcost:
                            s[s.index(node)].set_parent(current)
                    else:
                        s.append(node)

        return self.backtrack(current) if success else []


world = World(30, 30)
# world.plot_chart()
tracks = world.find_best_route()
world.plot_chart(tracks)
