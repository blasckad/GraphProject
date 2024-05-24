class Graph:
    def __init__(self):
        self._edges: dict[int, dict[int, list[int, int]]] = {}
        self._num_vertexes = 0
        self._num_edges = 0
        self._nodes_set = set()

    def set_stats(self, num_vert: int, num_edg: int):
        """
        Set number of vertexes and edges
        """
        self._num_vertexes = num_vert
        self._num_edges = num_edg

    def get_stats(self):
        """
        Return tuple of num_vertexes and num_edges
        """
        return self._num_vertexes, self._num_edges
    
    def add_edge(self, first_node: int, second_node: int, capacity: int):
        if first_node not in self._edges:
            self._edges[first_node] = {second_node : [capacity, capacity]}
        else:
            self._edges[first_node][second_node] = [capacity, capacity]
        self._nodes_set.add(first_node)
        self._nodes_set.add(second_node)

    def del_edge(self, first_node: int, second_node=None):
        if first_node in self._edges:
            if second_node and second_node in self._edges[first_node]:
                del self._edges[first_node][second_node]
            elif not second_node:
                del self._edges[first_node]

    def get_all_edges(self) -> dict[int, dict[int, list[int]]]:
        return self._edges
    
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
    
    def get_parent_nodes(self, node) -> set[int]:
        parents = set()
        for parent, child in self._edges.items():
            if node in list(child.keys()):
                parents.add(parent)
        return parents
    
    def get_node_degree(self, node: int) -> int:
        result = len(self._edges.get(node, {}).keys())
        for dic in list(self._edges.values()):
            for second_node in list(dic.keys()):
                if second_node == node:
                    result += 1
        return result
    
    def cut_function(self, subset: set) -> int:
        """
        Return the sum of weights of edges between subset
        and his superset (initial graph)
        """
        result = 0
        for first_node, dic in self._edges.items():
            for second_node, stats in dic.items():
                if first_node in subset and second_node not in subset or\
                first_node not in subset and second_node in subset:
                    result += stats[0]
        return result
    
    def conductance(self, subset: set) -> float:
        """
        Return ratio like cut(s, s')/min(vol(s), vol(s'))
        
        Args:
            subset: it's a set of cluster nodes
        """

        if self.vol_of_set(self._nodes_set.difference(subset)) == 0:
            return self.vol_of_set(subset)

        return self.cut_function(subset)/min(
            self.vol_of_set(subset),
            self.vol_of_set(self._nodes_set.difference(subset)))

    def vol_of_set(self, subset: set) -> int:
        """Calculate the sum of the degrees of all nodes in subset"""
        result = 0
        for node in subset:
            result += len(self.get_nodes_from_node(node))
        return result