from graph import *

graph = Graph()
graph.add_nodes(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'])

graph.add_edge('a', 'b')
graph.add_edge('a', 'c')
graph.add_edge('a', 'd')

graph.add_edge('b', 'e')
graph.add_edge('b', 'f')
graph.add_edge('e', 'i')

graph.add_edge('d', 'g')
graph.add_edge('d', 'h')
graph.add_edge('h', 'j')


result = graph.depth_first_search('a', 'j')

print(result)
