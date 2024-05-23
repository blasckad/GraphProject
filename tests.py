import networkx as nx
import random
import time
import os
from graph import Graph
from edmonds import edmonds_karp
from dinic import dinic_algorithm
import copy


def test(graph: Graph, iterations: int) -> dict:
    result = {}
    dinic_worse_time = 0
    edmonds_worse_time = 0
    dinic_average_time = 0
    edmonds_average_time = 0

    for _ in range(iterations):

        graph.set_edges_on_original_edges()
        
        start_time = time.time()
        result["edmonds_result"] = edmonds_karp(graph)
        end_time = time.time()
        elapsed_time = end_time - start_time

        if edmonds_worse_time < elapsed_time:
            edmonds_worse_time = elapsed_time
        if edmonds_average_time != 0:
            edmonds_average_time = (edmonds_average_time + elapsed_time)/2
        else:
            edmonds_average_time = elapsed_time

        graph.set_edges_on_original_edges()

        start_time = time.time()
        result["dinic_result"] = dinic_algorithm(graph)
        end_time = time.time()
        elapsed_time = end_time - start_time

        if dinic_worse_time < elapsed_time:
            dinic_worse_time = elapsed_time
        if dinic_average_time != 0:
            dinic_average_time = (dinic_average_time + elapsed_time)/2
        else:
            dinic_average_time = elapsed_time
        
    
    result["dinic_worse_time"] = dinic_worse_time
    result["dinic_average_time"] = dinic_average_time
    result["edmonds_worse_time"] = edmonds_worse_time
    result["edmonds_average_time"] = edmonds_average_time
    
    return result

def test_graphs_from_files() -> list:
    result = {}
    for dirpath, dirnames, filenames in os.walk("MaxFlow-tests"):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if filename != "test_d4.txt":
            # if True:
                graph = Graph()
                i=0
                with open(file_path, 'r') as file:
                    for line in file:
                        if i == 0:
                            graph.set_stats(*[int(k) for k in line.rstrip("\n").split(' ')], 1, int(line.rstrip("\n").split(' ')[0]))
                            i += 1
                        else:
                            f, s, cap = [int(k) for k in line.rstrip("\n").split(' ')]
                            graph.add_edge(f, s, cap)
                graph.set_original_edges()
                result[filename] = test(graph, 1)
    return result

def generate_graph(cnt_nodes: int, max_capacity: int, cnt_edges=0) -> Graph:
    graph = Graph()
    if cnt_edges > 0:
        gr = nx.gnm_random_graph(cnt_nodes, cnt_edges, directed=True)
        graph.set_stats(cnt_nodes, cnt_edges, 0, cnt_nodes - 1)
    else:
        gr = nx.gnm_random_graph(cnt_nodes, cnt_nodes**2//1.6, directed=True)
        graph.set_stats(cnt_nodes, cnt_nodes**2//1.6)
    edgelist = nx.to_edgelist(gr)
    for edge in edgelist:
        graph.add_edge(edge[0], edge[1], random.randint(3, max_capacity))
    graph.set_original_edges()
    return graph


def test_graphs_from_generate(cnt_nodes: int, max_capacity: int, cnt_edges: int, iterations: int) -> dict:
    result = {}
    dinic_worse_time = 0
    edmonds_worse_time = 0
    dinic_average_time = 0
    edmonds_average_time = 0
    for _ in range(iterations):
        graph = generate_graph(cnt_nodes, max_capacity, cnt_edges)
        graph.set_edges_on_original_edges()
        
        start_time = time.time()
        edmonds_karp(graph)
        end_time = time.time()
        elapsed_time = end_time - start_time

        if edmonds_worse_time < elapsed_time:
            edmonds_worse_time = elapsed_time
        if edmonds_average_time != 0:
            edmonds_average_time = (edmonds_average_time + elapsed_time)/2
        else:
            edmonds_average_time = elapsed_time

        graph.set_edges_on_original_edges()

        start_time = time.time()
        dinic_algorithm(graph)
        end_time = time.time()
        elapsed_time = end_time - start_time

        if dinic_worse_time < elapsed_time:
            dinic_worse_time = elapsed_time
        if dinic_average_time != 0:
            dinic_average_time = (dinic_average_time + elapsed_time)/2
        else:
            dinic_average_time = elapsed_time
    
    result["dinic_worse_time"] = dinic_worse_time
    result["dinic_average_time"] = dinic_average_time
    result["edmonds_worse_time"] = edmonds_worse_time
    result["edmonds_average_time"] = edmonds_average_time
    return result



if __name__ == "__main__":
    # tests = test_graphs_from_files()
    # # print(tests)
    # for filename, result in tests.items():
    #     print(filename, ': ', result)
    print(test_graphs_from_generate(1000, 5000, 100000, 50))