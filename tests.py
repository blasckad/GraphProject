import networkx as nx
import random
from graph import Graph
import time
from edmonds import edmonds_karp
from dinic import dinic_algorithm
import os

def test(graph: Graph, source: int, sink: int, iterations: int) -> dict:
    result = {}
    dinic_low_time = 0
    edmonds_low_time = 0
    dinic_average_time = 0
    edmonds_average_time = 0

    for _ in range(iterations):
        start_time = time.time()
        result["dinic_result"] = dinic_algorithm(graph, source, sink)
        end_time = time.time()
        elapsed_time = end_time - start_time

        if dinic_low_time < elapsed_time:
            dinic_low_time = elapsed_time
        if dinic_average_time != 0:
            dinic_average_time = (dinic_average_time + elapsed_time)/2
        else:
            dinic_average_time = elapsed_time
        
        start_time = time.time()
        result["edmonds_result"] = edmonds_karp(graph, source, sink)
        end_time = time.time()
        elapsed_time = end_time - start_time

        if edmonds_low_time < elapsed_time:
            edmonds_low_time = elapsed_time
        if edmonds_average_time != 0:
            edmonds_average_time = (edmonds_average_time + elapsed_time)/2
        else:
            edmonds_average_time = elapsed_time
    
    result["dinic_low_time"] = dinic_low_time
    result["dinic_average_time"] = dinic_average_time
    result["edmonds_low_time"] = edmonds_low_time
    result["edmonds_average_time"] = edmonds_average_time
    
    return result

def generate_graph(cnt_nodes: int, max_capacity: int, cnt_edges=0) -> Graph:
    graph = Graph()
    if cnt_edges > 0:
        gr = nx.gnm_random_graph(cnt_nodes, cnt_edges, directed=True)
        graph.set_stats(cnt_nodes, cnt_edges)
    else:
        gr = nx.gnm_random_graph(cnt_nodes, cnt_nodes**2//1.6, directed=True)
        graph.set_stats(cnt_nodes, cnt_nodes**2//1.6)
    edgelist = nx.to_edgelist(gr)
    for edge in edgelist:
        graph.add_edge(edge[0], edge[1], random.randint(3, max_capacity))
    return graph


def test_graphs_from_files() -> list:
    result = {}
    for dirpath, dirnames, filenames in os.walk("MaxFlow-tests"):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            g = Graph()
            i=0
            with open(file_path, 'r') as file:
                for line in file:
                    if i == 0:
                        g.set_stats(*line.split())
                        i+=1
                    else:
                        nums = line.split()
                        g.add_edge(int(nums[0]), int(nums[1]), int(nums[2]))
            result[file_path] = (test(g, 1, g._num_vertexes, 10))
    return result


def test_graphs_from_generate(cnt_nodes: int, max_capacity: int, cnt_edges: int) -> dict:
    g = generate_graph(cnt_nodes, max_capacity, cnt_edges)
    return test(g, 0, g._num_vertexes, 50)



if __name__ == "__main__":
    # tests = test_graphs_from_files()
    # print(tests)
    print(test_graphs_from_generate(100, 1000, 10000))