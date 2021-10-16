# Module for generation of bidirectional graph

class Graph:
    """Class for bi-directional graph"""
    def __init__(self):
        self.nodes = []
        self.edged = []


class Node:
    def __init__(self, name, heuristic=0):
        self.name = name
        self.heuristic = heuristic


class Edge:
    def __init__(self, source, target, value):
        self.source, self.target, self.value = source, target, value
