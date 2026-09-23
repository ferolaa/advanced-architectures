"""
Checks that every path found by the XGFT routing code matches a
real wire in the built network, and that the network reaches every
leaf from every other leaf.
"""

import networkx as nx

from networks.xgft import build_xgft_network
from routing.xgft_routing import route_xgft


def check_all_routes(h, m, w):
    graph = build_xgft_network(h, m, w)

    # the network should connect every leaf to every other leaf
    if not nx.is_connected(graph):
        print(f"PROBLEM: network for h={h}, m={m}, w={w} is not fully connected")
        return

    num_leaves = m ** h
    mistakes = 0
    for source in range(num_leaves):
        for destination in range(num_leaves):
            path = route_xgft(source, destination, h, m, w)
            for i in range(len(path) - 1):
                if not graph.has_edge(path[i], path[i + 1]):
                    print(f"PROBLEM: no wire from {path[i]} to {path[i + 1]}")
                    mistakes += 1
    if mistakes == 0:
        print(f"All routes for h={h}, m={m}, w={w} are correct, and the network is connected!")
    else:
        print(f"Found {mistakes} problems for h={h}, m={m}, w={w}.")


if __name__ == "__main__":
    check_all_routes(2, 2, 2)
    check_all_routes(3, 2, 2)
    check_all_routes(2, 3, 2)
