"""
XGFT (fat-tree) network builder.

A tree with h levels. Level 0 holds the leaves (m^h of them).
Each level up has fewer positions but more copies per position,
giving more parallel links near the top.

Parameters: h = height, m = branching factor (down), w = redundancy
factor (up). Number of switches at level i: N_i = m^(h-i) * w^i.
"""

import networkx as nx


def build_xgft_network(h, m, w):
    """
    Builds an XGFT with height h, branching m, redundancy w.
    Leaves are "leaf_<index>", switches are "L<level>_<position>_<copy>".
    """
    if h < 1 or m < 2 or w < 1:
        raise ValueError("h must be at least 1, m at least 2, w at least 1")

    graph = nx.Graph()

    num_leaves = m ** h
    for leaf in range(num_leaves):
        graph.add_node(f"leaf_{leaf}", stage=0)

    for level in range(1, h + 1):
        num_positions = m ** (h - level)
        num_copies = w ** level
        for position in range(num_positions):
            for copy in range(num_copies):
                graph.add_node(f"L{level}_{position}_{copy}", stage=level)

    # each level connected to the one below, copy by copy
    for level in range(1, h + 1):
        num_parent_positions = m ** (h - level)
        num_parent_copies = w ** level
        num_child_copies = w ** (level - 1)

        for position in range(num_parent_positions):
            child_positions = range(position * m, position * m + m)
            for child_position in child_positions:
                for child_copy in range(num_child_copies):
                    child_name = f"leaf_{child_position}" if level == 1 else f"L{level - 1}_{child_position}_{child_copy}"
                    for parent_copy in range(num_parent_copies):
                        graph.add_edge(child_name, f"L{level}_{position}_{parent_copy}")

    return graph


if __name__ == "__main__":
    # manual check
    net = build_xgft_network(h=2, m=2, w=2)
    print("Number of switches (incl. leaves):", net.number_of_nodes())
    print("Number of wires:", net.number_of_edges())
