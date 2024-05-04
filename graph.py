class Graph:
    def __init__(self):
        self.edges: dict[int, dict[int, list[int, int]]] = {}
    
    def add_edge(self, first_node, second_node, capacity):
        if first_node not in self.edges:
            self.edges[first_node] = {second_node : [0, capacity]}
        else:
            self.edges[first_node][second_node] = [0, capacity]
    
    def change_flow(self, first_node, second_node, delta_flow):
        self.edges[first_node][second_node][0] += delta_flow
    
    def get_nodes_from_node(self, node): 
       return list(self.edges[node].keys())

# g = Graph()

# g.add_edge(1,2,3)
# g.add_edge(1,3,3)

# print(g.get_nodes_from(1))