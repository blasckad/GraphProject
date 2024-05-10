from graph import Graph
from collections import deque

def bfs(graph: Graph, source: int, stock: int, level: list[int]):
    """
    Create a layered network and return is there exist a path
    """
    queue = deque([source])
    for i in range(len(level)):
        level[i] = -1
    level[source - 1] = 0
    while queue:
        u = queue.popleft()
        for v in graph.get_nodes_from_node(u):
            if level[v - 1] == -1:
                level[v - 1] = level[u - 1] + 1
                queue.append(v)
    return level[stock - 1] != -1


def dinic(graph: Graph, source: int, stock: int):
    flow = 0

    # no more than |V| entries to the main phase of algorithm
    stop_cnt = graph.get_stats()[0]

    level = [-1] * stop_cnt

    # while exist path in the layered network
    while bfs(graph, source, stock, level) and stop_cnt > 0:
        stop_cnt -= 1

        # DFS from source in layered network
        stack = [source]
        path = []
        while stack:
            u = stack.pop()
            path.append(u)
            for v in graph.get_nodes_from_node(u):
                # if it's reverse edge to previous vertex
                if len(path) > 1 and path[-2] == v:
                    continue 
                if level[v - 1] >= level[u - 1] + 1:
                    stack.append(v)
                    # if we went to stock
                    if v == stock:
                        path_flow = 1000000
                        # path = [v]
                        path.append(v)

                        # # Поиск блокирующего потока путем обхода графа в обратном направлении
                        # while path[-1] != source:
                        #     for prev in graph.get_parent_nodes(path[-1]):
                        #         if level[prev - 1] <= level[path[-1] - 1] - 1:
                        #             path.append(prev)
                        #             break
                        # path = path[::-1]
                        path_len = len(path)

                        # Определение блокирующего потока на найденном пути
                        for i in range(path_len - 1, 0, -1):
                            path_flow = min(
                                path_flow,
                                graph.get_edge_stat(path[i - 1], path[i])[0]
                            )
                        
                        # Обновление пропускных способностей ребер и обратных ребер
                        for i in range(path_len - 1, 0, -1):
                            graph.change_flow(path[i - 1], path[i], path_flow)
                        flow += path_flow
                        # restart DFS from source
                        stack = [source]
                        path.clear()
                        break
            # couldn't go to stock
            if not stack:
                for v in graph.get_parent_nodes(u):
                    if level[v - 1] == level[u - 1] - 1 \
                            and path[0] != v:
                        stack = [v]
                        break
                level[u - 1] = -1
                path.clear()
    return flow


g = Graph()
g.add_edge(1, 2, 5)
g.add_edge(2, 3, 3)
g.add_edge(3, 4, 5)
g.add_edge(1, 5, 2)
g.add_edge(5, 4, 1)
g.add_edge(5, 3, 1)
g.add_edge(2, 6, 2)
g.add_edge(6, 3, 1)
g.add_edge(6, 4, 1)
g.set_stats(6, 9)
print(dinic(g, 1, 4))
# i = 0
# with open("test_flow.txt", 'r') as file:
#     for line in file:
#         if i == 0:
#             g.set_stats(*[int(k) for k in line.rstrip("\n").split(' ')])
#             i += 1
#         else:
#             f, s, cap = [int(k) for k in line.rstrip("\n").split(' ')]
#             g.add_edge(f, s, cap)
# print("graph was read")
# import time
# start = time.time()
# res = dinic(g, 1, 4952)
# print(time.time() - start)
# print(res)