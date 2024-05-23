import copy

class Graph:
    def __init__(self):
        self._edges: dict[int, dict[int, list[int, int]]] = {}
        self._original_edges: dict[int, dict[int, list[int, int]]] = {}
        self._num_vertexes = 0
        self._num_edges = 0
        self._source = 0
        self._sink = 0

    def set_stats(self, num_vert: int, num_edg: int, source: int, sink: int):
        """
        Set number of vertexes and edges
        """
        self._num_vertexes = num_vert
        self._num_edges = num_edg
        self._source = source
        self._sink = sink

    def get_stats(self):
        """
        Return tuple of num_vertexes and num_edges
        """
        return self._num_vertexes, self._num_edges, self._source, self._sink
    
    def set_original_edges(self):
        self._original_edges = copy.deepcopy(self._edges)
    
    def set_edges_on_original_edges(self):
        self._edges = copy.deepcopy(self._original_edges)
    
    def add_edge(self, first_node: int, second_node: int, capacity: int):
        if first_node not in self._edges:
            self._edges[first_node] = {second_node : [capacity, capacity]}
        else:
            self._edges[first_node][second_node] = [capacity, capacity]

    def del_edge(self, first_node: int, second_node=None):
        if first_node in self._edges:
            if second_node and second_node in self._edges[first_node]:
                del self._edges[first_node][second_node]
            elif not second_node:
                del self._edges[first_node]

    def get_all_edges(self) -> dict[int, dict[int, list[int]]]:
        return self._edges.copy()
    
    def get_edge_stat(self, first_node: int, second_node: int) -> list[int]:
        """
        Function return a list of flow and capacity like [flow, capacity]
        """
        return self._edges[first_node][second_node]

    def change_flow(self, first_node: int, second_node: int, delta_flow: int):
        self._edges[first_node][second_node][0] -= delta_flow
        # checking the existing reverse edge
        if second_node in self._edges:
            if first_node in self._edges[second_node]:
                self._edges[second_node][first_node][0] += delta_flow
            else:
                self._edges[second_node][first_node] = [
                    delta_flow,
                    self._edges[first_node][second_node][1]
                ]
        else:
            self._edges[second_node] = {
                first_node:
                [
                    delta_flow,
                    self._edges[first_node][second_node][1]
                ]
            }
        if self._edges[first_node][second_node][0] == 0:
            del self._edges[first_node][second_node]

    def get_nodes_from_node(self, node: int) -> list[int]:
        if node not in self._edges:
            return []
        return list(self._edges[node].keys())
    
    def get_parent_nodes(self, node):
        parents = []
        for parent, child in self._edges.items():
            if node in list(child.keys()):
                parents.append(parent)
        return parents
