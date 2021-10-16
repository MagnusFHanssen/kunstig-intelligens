# Module for graph generation and search


class Graph:
    """Class for a simple graph used in graph-search"""
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.node_count = 0
        self.edge_count = 0

    def add_node(self, name):
        self.nodes.append(Node(name))
        self.node_count += 1

    def add_nodes(self, name_list):
        for name in name_list:
            self.nodes.append(Node(name))
            self.node_count += 1

    def add_edge(self, source, target):
        if isinstance(source, int) and isinstance(target, int):
            self.edges.append(Edge(source, target))
            self.edge_count += 1
        elif isinstance(source, str) and isinstance(target, str):
            self.edges.append(Edge(self.get_index(source), self.get_index(target)))
            self.edge_count += 1
        else:
            raise TypeError("Source and target must both be strings or integers")

    def get_index(self, name):
        indices = [index for index, node in enumerate(self.nodes) if node.name == name]
        if len(indices) == 0:
            raise ValueError("Node {} does not exist".format(name))
        else:
            return indices[0]

    def get_children(self, node):
        edge_list = [index for index, edge in enumerate(self.edges) if edge.source == node]
        edges = [self.edges[edge].target for edge in edge_list]
        edges.sort(reverse=True)
        return edges

    def __get_names(self, node_indices):
        return [self.nodes[node_index].name for node_index in node_indices]

    def depth_first_search(self, start, goal):
        if isinstance(start, str):
            start_node = self.get_index(start)
        elif isinstance(start, int):
            start_node = start
        else:
            return None

        if isinstance(goal, str):
            goal_node = self.get_index(goal)
        elif isinstance(goal, int):
            goal_node = goal
        else:
            return None

        s = []
        h = []
        s.append(start_node)

        while s:
            curr_node = s.pop()
            if curr_node == goal_node:
                h.append(curr_node)
                return self.__get_names(h)
            if curr_node in h:
                continue
            h.append(curr_node)
            s += self.get_children(curr_node)
        return None


class Node:
    """Class for a simple node in a graph"""
    def __init__(self, name):
        self.name = name


class Edge:
    def __init__(self, source, target):
        self.source = source
        self.target = target

