class Graph:
    def __init__(self):
        self._edges: dict[int, dict[int, list[int, int]]] = {}
    
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

    def get_nodes_from_node(self, node: int) -> list[int]:
        straight_edges = []
        for second_node, stats in self._edges[node].items():
            # if it's possible to saturate the flow
            if stats[0] > 0:
                straight_edges.append(second_node)
        return straight_edges
