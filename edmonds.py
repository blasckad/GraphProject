from graph import Graph
from collections import deque
import time


def edmonds_karp(graph: Graph) -> int:
    """
    Function transforms input graph to residual network
    and return value of maximum flow
    """
    source = graph._source
    stock = graph._sink
    max_flow = 0
    queue = deque()
    visited = {}
    while True:
        queue.append(source)
        # key is child node, value is parent node
        visited[source] = None
        while queue and stock not in visited:
            pivot = queue.popleft()
            for node in graph.get_nodes_from_node(pivot):
                if node not in visited:
                    visited[node] = pivot
                    queue.append(node)
        if stock in visited:
            child = queue.pop()
            parent = visited[child]
            path = deque([child])
            # delta_flow is minimum residual flow
            delta_flow = graph.get_edge_stat(parent, child)[0]
            # Only a source has None parent
            while parent is not None:
                delta_flow = min(delta_flow, graph.get_edge_stat(parent, child)[0])
                child = parent
                parent = visited[child]
                path.appendleft(child)
            max_flow += delta_flow
            # Changing the residual network
            for i in range(len(path) - 1):
                graph.change_flow(path[i], path[i + 1], delta_flow)
            queue.clear()
            visited.clear()
        else:
            break
    
    return max_flow


# if __name__ == "__main__":
#     g = Graph()
#     i = 0
#     with open("MaxFlow-tests/test_rl07.txt", 'r') as file:
#         for line in file:
#             if i == 0:
#                 g.set_stats(*[int(k) for k in line.rstrip("\n").split(' ')])
#                 i += 1
#             else:
#                 f, s, cap = [int(k) for k in line.rstrip("\n").split(' ')]
#                 g.add_edge(f, s, cap)
#     start = time.time()
#     res = edmonds_karp(g, 1, g.get_stats()[0])
#     print(time.time() - start)
#     print(res)
