from graph import Graph
import networkx as nx

def to_nx_graph(graph: Graph) -> nx.DiGraph:
    result = nx.DiGraph()
    for f_node, dct in graph.get_all_edges().items():
        for s_node, stats in dct.items():
            result.add_edge(f_node, s_node, weight=stats[1])
    return result


def conductance(graph: Graph, S: list[int] | set[int]) -> float:
    """
    Return the value of conductance
    the smaller the better
    """
    digraph = to_nx_graph(graph)
    return nx.conductance(digraph, S, weight="weight")


def modularity(graph: Graph, S: list[int] | set[int]) -> float:
    """
    Return the value of modularity
    the bigger the better
    returning value is in the interwal between -1 and 1
    """
    digraph = to_nx_graph(graph)
    S_addition = set(digraph.nodes.keys()).difference(set(S))
    return nx.community.modularity(digraph, [S, S_addition])
