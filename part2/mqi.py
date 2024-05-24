from graph_improve import Graph
from dinic import dinic_algorithm, deque
from metrics import conductance

def mqi(graph: Graph, R: set) -> set:
    """

    Args:
        R: The original set of elements.
        cut_function: A function that calculates the cut value of a subset S of R.
        vol_function: A function that calculates the volume of a subset S of R.
        conductance: A function that evaluates the quality of a subset S as a QIS.

    Returns:
        The best found MQIS.
    """

    def augmenting(delta: float) -> Graph:
        nonlocal R
        source = -1
        supersink = -2
        subgraph = Graph()
        # subgraph R selection and adding super sink
        for first_node, dic in graph.get_all_edges().items():
            for second_node in list(dic.keys()):
                if first_node in R:
                    subgraph.add_edge(source,
                                      first_node,
                                      delta*graph.get_node_degree(first_node)
                                      )
                    if second_node in R:
                        subgraph.add_edge(source,
                                      second_node,
                                      delta*graph.get_node_degree(second_node)
                                      )
                        subgraph.add_edge(first_node, second_node, delta*graph.get_node_degree(first_node))
                        subgraph.add_edge(second_node, first_node, delta*graph.get_node_degree(second_node))
                    else:
                        subgraph.add_edge(
                            first_node,
                            supersink,
                            10**9)
        return subgraph
        
    Sk = R  # Initial candidate is the whole set
    delta_k = graph.conductance(Sk)/10
    print(delta_k)

    subgraph = augmenting(delta_k)

    while True:
        dinic_algorithm(subgraph, -1, -2)
        # find cut by bfs
        queue = deque([-1])
        visited = set()
        while queue:
            pivot = queue.popleft()
            visited.add(pivot)
            for node in subgraph.get_nodes_from_node(pivot):
                if node not in visited:
                    visited.add(node)
                    queue.append(node)
        # Find the subset that minimizes the objective function
        # Sk_next = min(
        #     (subset, visited - delta_k * graph.vol_function(subset))
        #     for subset in powerset(R)
        # )[0]
        Sk_next = visited
        print(visited)

        if graph.conductance(Sk_next) < delta_k:
            # Update the threshold if the new subset is better
            delta_k = graph.conductance(Sk_next)
            Sk = Sk_next
        else:
            # The current threshold is considered optimal, return the previous solution
            return Sk
        

if __name__ == "__main__":
    gr = Graph()
    cnt_edges = 0
    with open("part2/edge_list.txt", 'r') as file:
        for line in file:
            fnode, snode = list(map(int, line.split()))
            gr.add_edge(fnode, snode, 10)
            gr.add_edge(snode, fnode, 10)
            cnt_edges += 1
    cluster = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 34}
    gr.set_stats(num_edg=cnt_edges)
    print(mqi(gr, cluster))
