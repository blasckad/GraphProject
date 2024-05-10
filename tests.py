import networkx as nx
import random
from graph import Graph
import time
from edmonds import edmonds_karp
from dinic import dinic_algorithm

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

g = Graph()

with open('../test_rl10.txt', 'r') as file:
    for line in file:
        nums = line.split()
        # print(nums)

        g.add_edge(int(nums[0]), int(nums[1]), int(nums[2]))

start_time = time.time()

print(dinic_algorithm(g, 1, 4952))

end_time = time.time()

elapsed_time = end_time - start_time

print(elapsed_time)
