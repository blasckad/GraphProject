from graph_improve import Graph
from dinic import dinic_algorithm, deque

def mqi(graph: Graph, R: set) -> set:
    """
    Finds a maximal quasi-independent set (MQIS) using the MQI algorithm.

    Args:
        R: The original set of elements.
        cut_function: A function that calculates the cut value of a subset S of R.
        vol_function: A function that calculates the volume of a subset S of R.
        conductance: A function that evaluates the quality of a subset S as a QIS.

    Returns:
        The best found MQIS.
    """

    def powerset(s):
        """Returns the power set of a set."""
        x = len(s)
        masks = [1 << i for i in range(x)]
        for i in range(1 << x):
            yield {s[j] for j in range(x) if (i & masks[j])}

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
                                      delta*graph.get_node_degree(first_node)
                                      )
                        subgraph.add_edge(first_node, second_node, 1)
                    else:
                        subgraph.add_edge(
                            first_node,
                            supersink,
                            len(set(graph.get_nodes_from_node(first_node)).difference(R)))
                elif second_node in R:
                    subgraph.add_edge(source,
                                      second_node,
                                      delta*graph.get_node_degree(first_node)
                                      )
                    subgraph.add_edge(second_node,
                                      supersink,
                                      len(graph.get_parent_nodes(second_node)\
                                          .difference(R)))
        

    k = 1
    Sk = R  # Initial candidate is the whole set
    delta_k = graph.conductance(Sk)

    subgraph = augmenting(delta_k)

    while True:
        dinic_algorithm(subgraph, -1, -2)
        left_part = set()
        # find cut by bfs
        queue = deque([-1])
        visited = set()
        while queue:
            pivot = queue.popleft()
            visited.add(pivot)
            left_part.add(pivot)
            for node in subgraph.get_nodes_from_node(pivot):
                if node not in visited:
                    visited.add(node)
                    queue.append(node)
        # Find the subset that minimizes the objective function
        # neccessary to create subtraction left_part and delta_k*...
        Sk_next = min(
            (subset, left_part - delta_k * graph.vol_function(subset))
            for subset in powerset(R)
        )[0]

        if subgraph.conductance(Sk_next) < delta_k:
            # Update the threshold if the new subset is better
            delta_k = subgraph.conductance(Sk_next)
            Sk = Sk_next
            k += 1
        else:
            # The current threshold is considered optimal, return the previous solution
            return Sk