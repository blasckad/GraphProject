from collections import deque
from graph import Graph


def dinic_algorithm(graph: Graph, source: int, sink: int):
    def build_level_graph(level_graph, source):
        level_graph.clear()
        level_graph[source] = 0
        queue = deque([source])
        while queue:
            current_node = queue.popleft()
            for next_node in graph.get_nodes_from_node(current_node):
                edge_capacity = graph.get_edge_stat(current_node, next_node)[1]
                if edge_capacity > 0 and next_node not in level_graph:
                    level_graph[next_node] = level_graph[current_node] + 1
                    queue.append(next_node)

    def blocking_flow(current_node, target, flow, level_graph):
        if current_node == target:
            return flow
        current_flow = 0
        for next_node in graph.get_nodes_from_node(current_node):
            edge_capacity = graph.get_edge_stat(current_node, next_node)[0]
            if level_graph.get(next_node, -1) == level_graph[current_node] + 1 and edge_capacity > 0:
                delta_flow = blocking_flow(next_node, target, min(flow, edge_capacity), level_graph)
                if delta_flow > 0:
                    graph.change_flow(current_node, next_node, delta_flow)
                    current_flow += delta_flow
                    flow -= delta_flow
                    if flow == 0:
                        break
        return current_flow

    max_flow = 0
    level_graph = {}
    while True:
        build_level_graph(level_graph, source)
        if sink not in level_graph:
            break
        while True:
            delta_flow = blocking_flow(source, sink, float('inf'), level_graph)
            if delta_flow == 0:
                break
            max_flow += delta_flow
    return max_flow