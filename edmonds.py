from graph import Graph
from collections import deque


def edmonds_karp(graph: Graph, source: int, stock: int) -> int:
    """
    Function transforms input graph to residual network
    and return value of maximum flow
    """
    max_flow = 0
    for _ in range(5000):
        queue = deque([source])
        # visited is dict like {child: parent}
        visited = {source: None}
        next_iteration = True
        path = deque()
        # find shortest path
        while queue and next_iteration:
            pivot = queue.popleft()
            for node in graph.get_nodes_from_node(pivot):
                if node not in visited:
                    visited[node] = pivot
                    queue.append(node)
                    if node == stock:
                        next_iteration = False
                        break
        if queue:
            child = queue.popleft()
            parent = visited[child]
            path.appendleft(child)
            # delta_flow is minimum residual flow
            delta_flow = graph.get_edge_stat(parent, child)[0]
            # Only a source has None parent
            while parent is not None:
                delta = graph.get_edge_stat(parent, child)
                if delta_flow > delta[0]:
                    delta_flow = delta[0]
                child = parent
                parent = visited[child]
                path.appendleft(child)
            max_flow += delta_flow
            # Changing the residual network
            for i in range(len(path) - 1):
                graph.change_flow(path[i], path[i + 1], delta_flow)
        else:
            # there isn't any path between source and stock
            return max_flow
    
    return max_flow
