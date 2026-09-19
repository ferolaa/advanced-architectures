"""
Checks that every path found by the routing code matches a real
wire in the built network.
"""

from networks.baseline import build_baseline_network
from routing.baseline_routing import route_baseline


def check_all_routes(n):
    graph = build_baseline_network(n)
    mistakes = 0
    for source in range(n):
        for destination in range(n):
            path = route_baseline(source, destination, n)
            for i in range(len(path) - 1):
                if not graph.has_edge(path[i], path[i + 1]):
                    print(f"PROBLEM: no wire from {path[i]} to {path[i + 1]}")
                    mistakes += 1
    if mistakes == 0:
        print(f"All routes for n={n} are correct!")
    else:
        print(f"Found {mistakes} problems for n={n}.")


if __name__ == "__main__":
    check_all_routes(8)
    check_all_routes(16)
