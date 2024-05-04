import networkx as nx
import random
from graph import Graph

# def generate_graph(node_count, edges_count):
#     if node_count < 2:
#         return
    
#     graph = Graph()

#     source = 0
#     stok = node_count - 1
#     way = set()
#     way.add(source)
#     way.add(stok)

#     count_first_way = random.randint(1, edges_count)
#     edges_count -= count_first_way

#     current_node = random.randint(1, node_count - 2)
#     way.add(current_node)
#     graph.add_edge(source, current_node, random.randint(1, 100))

#     for i in range(count_first_way - 2):
#         new_node = random.randint(1, node_count - 2)
#         while new_node in way:
#             new_node = random.randint(1, node_count - 2)
#         way.add(new_node)
#         graph.add_edge(current_node, new_node, random.randint(1, 100))
#         current_node = new_node
    
#     graph.add_edge(current_node, stok, random.randint(1, 100))

#     return graph

# g = generate_graph(10, 15)

# print(g._graph)


g = nx.dense_gnm_random_graph(10, 20, 5)

print(g.edges)


