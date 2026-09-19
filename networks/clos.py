"""
Clos network builder.

Three stages of switches:
- input stage: r switches, each taking n inputs
- middle stage: m switches, each connected to every input and output switch
- output stage: r switches

Total inputs = r * n.
"""

import networkx as nx


def build_clos_network(r, n, m):
    """
    Builds a 3-stage Clos network.
    r = input/output switches, n = inputs per input switch, m = middle switches.
    Switches named "in_i", "mid_j", "out_k".
    """
    if r < 1 or n < 1 or m < 1:
        raise ValueError("r, n and m must all be at least 1")

    graph = nx.DiGraph()

    for i in range(r):
        graph.add_node(f"in_{i}", stage=0)
    for j in range(m):
        graph.add_node(f"mid_{j}", stage=1)
    for k in range(r):
        graph.add_node(f"out_{k}", stage=2)

    # every input switch to every middle switch
    for i in range(r):
        for j in range(m):
            graph.add_edge(f"in_{i}", f"mid_{j}")

    # every middle switch to every output switch
    for j in range(m):
        for k in range(r):
            graph.add_edge(f"mid_{j}", f"out_{k}")

    return graph


def total_inputs(r, n):
    """Total number of inputs (r * n)."""
    return r * n


if __name__ == "__main__":
    # manual check
    r, n, m = 4, 3, 5
    net = build_clos_network(r, n, m)
    print("Total inputs:", total_inputs(r, n))
    print("Number of switches:", net.number_of_nodes())
    print("Number of wires:", net.number_of_edges())
