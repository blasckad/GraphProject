import networkx as nx
import random
import time
import os
from graph import Graph
from edmonds import edmonds_karp
from dinic import dinic_algorithm
import copy
import numpy as np



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
        
        edmonds_average_time += elapsed_time

        graph.set_edges_on_original_edges()

        start_time = time.time()
        dinic_algorithm(graph)
        end_time = time.time()
        elapsed_time = end_time - start_time

        if dinic_worse_time < elapsed_time:
            dinic_worse_time = elapsed_time

        dinic_average_time += elapsed_time
    
    result["dinic_worse_time"] = dinic_worse_time
    result["dinic_average_time"] = dinic_average_time/iterations
    result["edmonds_worse_time"] = edmonds_worse_time
    result["edmonds_average_time"] = edmonds_average_time/iterations
    return result



if __name__ == "__main__":
    # tests = test_graphs_from_files()
    # for filename, result in tests.items():
    #     print(filename, ': ', result)

    # print(test_graphs_from_generate(1000, 40000, 10000, 50))

    nodes = 500
    edges = 50000
    max_capacity = 100

    stats = [nodes, max_capacity, edges]

    result = []
    for i in range(3):
        m = 1
        for _ in range(3):
            stats[i] *= m
            result.append(test_graphs_from_generate(stats[0], stats[1], stats[2], 20))
            print(stats)
            m *= 10
            stats = [nodes, max_capacity, edges]

    print
    
    for i in range(3):
        # print("Увеличение в 10 раз")
        # print("edmonds:", (result[(i*3)+1]["edmonds_average_time"] - result[0]["edmonds_average_time"])/result[0]["edmonds_average_time"])
        # print("dinic:", (result[(i*3)+1]["dinic_average_time"] - result[0]["dinic_average_time"])/result[0]["dinic_average_time"])
        # print("Увеличение в 100 раз")
        # print("edmonds:", (result[(i*3)+2]["edmonds_average_time"] - result[0]["edmonds_average_time"])/result[0]["edmonds_average_time"])
        # print("dinic:", (result[(i*3)+2]["dinic_average_time"] - result[0]["dinic_average_time"])/result[0]["dinic_average_time"])

        print(stats[i])
        print("Разница:", (result[(i*3)]["edmonds_average_time"])/result[(i*3)]["dinic_average_time"])
        print("Увеличение в 10 раз")
        print("Разница:", (result[(i*3)+1]["edmonds_average_time"])/result[(i*3)+1]["dinic_average_time"])
        print("Увеличение в 100 раз")
        print("Разница:", (result[(i*3)+2]["edmonds_average_time"])/result[(i*3)+2]["dinic_average_time"])
        
        

    
    


    
