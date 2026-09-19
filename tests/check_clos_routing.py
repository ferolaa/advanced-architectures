"""
Checks that every path found by the Clos routing code matches a
real wire in the built network.
"""

from networks.clos import build_clos_network
from routing.clos_routing import route_clos


def check_all_routes(r, n, m):
    graph = build_clos_network(r, n, m)
    mistakes = 0
    total_inputs = r * n
    for source in range(total_inputs):
        for destination in range(total_inputs):
            path = route_clos(source, destination, r, n, m)
            for i in range(len(path) - 1):
                if not graph.has_edge(path[i], path[i + 1]):
                    print(f"PROBLEM: no wire from {path[i]} to {path[i + 1]}")
                    mistakes += 1
    if mistakes == 0:
        print(f"All routes for r={r}, n={n}, m={m} are correct!")
    else:
        print(f"Found {mistakes} problems for r={r}, n={n}, m={m}.")


if __name__ == "__main__":
    check_all_routes(4, 3, 5)
    check_all_routes(3, 2, 4)
