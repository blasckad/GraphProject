from graph import Graph


def edmonds_karp(graph: Graph, source: int, stock: int) -> int:
    """
    Function transforms input graph to residual network
    and return value of maximum flow
    """
    max_flow = 0
    for _ in range(100000):
        queue = [source]
        # visited is dict like {child: parent}
        visited = {source: None}
        next_iteration = True
        path: list[int] = []
        # find shortest path
        while queue and next_iteration:
            pivot = queue.pop(0)
            for node in graph.get_nodes_from_node(pivot):
                if node not in visited:
                    visited[node] = pivot
                    queue.append(node)
                    if node == stock:
                        next_iteration = False
                        break
        if queue:
            child = queue.pop()
            parent = visited[child]
            path.append(child)
            # delta_flow is minimum residual flow
            delta_flow = graph.get_edge_stat(parent, child)
            delta_flow = min(delta_flow[1], delta_flow[0])
            # Only a source has None parent
            while parent is not None:
                delta = graph.get_edge_stat(parent, child)
                if delta_flow > min(delta[1], delta[0]):
                    delta_flow = min(delta[1], delta[0])
                child = parent
                parent = visited[child]
                path.append(child)
            path = path[::-1]
            max_flow += delta_flow
            # Changing the residual network
            for i in range(len(path) - 1):
                graph.change_flow(path[i], path[i + 1], delta_flow)
        else:
            # there isn't any path between source and stock
            return max_flow
    
    return max_flow
