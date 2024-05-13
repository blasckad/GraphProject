import networkx as nx
import random
from graph import Graph
import time
from edmonds import edmonds_karp
from dinic import dinic_algorithm
import pytest

@pytest.mark.parametrize(
    "init, edges, expected",
    [
        (
            (9, 17),
            [
                (0, 4, 16), (0, 3, 12), (0, 2, 4), (4, 7, 5), (4, 6, 3), (4, 3, 1),
                (3, 4, 17), (3, 1, 13), (3, 2, 4), (2, 3, 15), (7, 6, 7), (6, 1, 14),
                (1, 6, 6), (6, 8, 9), (1, 8 , 20), (5, 8, 12), (2, 5, 20)
            ],
            25
        ),
        (
            (9, 17),
            [
                (0, 6, 2), (0, 7, 20), (0, 1, 16), (6, 3, 17), (6, 4, 20), (6, 7, 20),
                (7, 6, 17), (7, 5, 12), (7, 1, 15), (1, 7, 13), (3, 4, 15), (4, 5, 6),
                (5, 4, 10), (4, 8, 15), (5, 8, 6), (2, 8, 20), (1, 2, 5)
            ],
            26
        ),
        (
            (9, 17),
            [
                (0, 3, 15), (0, 7, 19), (0, 1, 14), (3, 5, 20), (3, 6, 19), (3, 7, 3),
                (7, 3, 3), (7, 4, 19), (7, 1, 12), (1, 7, 15), (5, 6, 16), (6, 4, 12),
                (4, 6, 4), (6, 8, 8), (4, 8, 14), (2, 8, 3), (1, 2, 19)
            ],
            25
        ),
        (
            (9, 17),
            [
                (0, 5, 13), (0, 4, 6), (0, 3, 2), (5, 6, 14), (5, 1, 4), (5, 4, 18),
                (4, 5, 2), (4, 2, 11), (4, 3, 8), (6, 1, 10), (1, 2, 20), (2, 1, 17),
                (1, 8, 10), (2, 8, 9), (7, 8, 13), (3, 7, 5)
            ],
            21
        ),
        (
            (9, 17),
            [
                (0, 3, 17), (0, 1, 14), (0, 4, 18), (3, 5, 6), (3, 7, 14), (3, 1, 12),
                (1, 3, 2), (1, 2, 15), (1, 4, 17), (4, 1, 20), (5, 7, 8), (7, 2, 4),
                (2, 7, 14), (7, 8, 10), (2, 8, 20), (6, 8, 6), (4, 6, 16)
            ],
            35
        ),
        (
            (9, 17),
            [
                (0, 1, 6), (0, 6, 5), (0, 4, 13), (1, 2, 7), (1, 3, 19), (1, 6, 19),
                (6, 1, 2), (6, 7, 17), (6, 4, 20), (4, 6, 13), (2, 3, 14), (3, 7, 9),
                (7, 3, 9), (3, 8, 1), (7, 8, 6), (5, 8, 4), (4, 5, 16)
            ],
            11
        )
    ]
)
def test_edmonds(init, edges, expected):
    g = Graph()
    g.set_stats(init[0], init[1])
    for ed in edges:
        g.add_edge(ed[0], ed[1], ed[2])

    assert edmonds_karp(g, 0, 8) == expected


@pytest.mark.parametrize(
    "init, edges, expected",
    [
        (
            (9, 17),
            [
                (0, 4, 16), (0, 3, 12), (0, 2, 4), (4, 7, 5), (4, 6, 3), (4, 3, 1),
                (3, 4, 17), (3, 1, 13), (3, 2, 4), (2, 3, 15), (7, 6, 7), (6, 1, 14),
                (1, 6, 6), (6, 8, 9), (1, 8 , 20), (5, 8, 12), (2, 5, 20)
            ],
            25
        ),
        (
            (9, 17),
            [
                (0, 6, 2), (0, 7, 20), (0, 1, 16), (6, 3, 17), (6, 4, 20), (6, 7, 20),
                (7, 6, 17), (7, 5, 12), (7, 1, 15), (1, 7, 13), (3, 4, 15), (4, 5, 6),
                (5, 4, 10), (4, 8, 15), (5, 8, 6), (2, 8, 20), (1, 2, 5)
            ],
            26
        ),
        (
            (9, 17),
            [
                (0, 3, 15), (0, 7, 19), (0, 1, 14), (3, 5, 20), (3, 6, 19), (3, 7, 3),
                (7, 3, 3), (7, 4, 19), (7, 1, 12), (1, 7, 15), (5, 6, 16), (6, 4, 12),
                (4, 6, 4), (6, 8, 8), (4, 8, 14), (2, 8, 3), (1, 2, 19)
            ],
            25
        ),
        (
            (9, 17),
            [
                (0, 5, 13), (0, 4, 6), (0, 3, 2), (5, 6, 14), (5, 1, 4), (5, 4, 18),
                (4, 5, 2), (4, 2, 11), (4, 3, 8), (6, 1, 10), (1, 2, 20), (2, 1, 17),
                (1, 8, 10), (2, 8, 9), (7, 8, 13), (3, 7, 5)
            ],
            21
        ),
        (
            (9, 17),
            [
                (0, 3, 17), (0, 1, 14), (0, 4, 18), (3, 5, 6), (3, 7, 14), (3, 1, 12),
                (1, 3, 2), (1, 2, 15), (1, 4, 17), (4, 1, 20), (5, 7, 8), (7, 2, 4),
                (2, 7, 14), (7, 8, 10), (2, 8, 20), (6, 8, 6), (4, 6, 16)
            ],
            35
        ),
        (
            (9, 17),
            [
                (0, 1, 6), (0, 6, 5), (0, 4, 13), (1, 2, 7), (1, 3, 19), (1, 6, 19),
                (6, 1, 2), (6, 7, 17), (6, 4, 20), (4, 6, 13), (2, 3, 14), (3, 7, 9),
                (7, 3, 9), (3, 8, 1), (7, 8, 6), (5, 8, 4), (4, 5, 16)
            ],
            11
        )
    ]
)
def test_dinic(init, edges, expected):
    g = Graph()
    g.set_stats(init[0], init[1])
    for ed in edges:
        g.add_edge(ed[0], ed[1], ed[2])

    assert dinic_algorithm(g, 0, 8) == expected

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


if __name__ == "__main__":
    g = Graph()
    i=0
    with open('test_flow.txt', 'r') as file:
        for line in file:
            if i == 0:
                g.set_stats(*line.split())
                i+=1
            else:
                nums = line.split()
                # print(nums)

                g.add_edge(int(nums[0]), int(nums[1]), int(nums[2]))

    start_time = time.time()

    print(dinic_algorithm(g, 1, 4952))

    end_time = time.time()

    elapsed_time = end_time - start_time

    print(elapsed_time)
