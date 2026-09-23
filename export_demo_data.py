"""
Builds each network with example settings and writes out its
layout (node positions), wires, and every valid path, as JSON.

This is used by network_demo.html so the animation shows real
paths from the real routing code — not a re-implementation of the
algorithms in JavaScript.
"""

import json

import networkx as nx

from networks.baseline import build_baseline_network
from networks.benes import build_benes_network
from networks.clos import build_clos_network
from networks.xgft import build_xgft_network
from routing.baseline_routing import route_baseline
from routing.clos_routing import route_clos
from routing.xgft_routing import route_xgft


def layout_by_stage(graph):
    """Positions nodes left to right by stage, stacked top to bottom within a stage."""
    stages = {}
    for node, data in graph.nodes(data=True):
        stages.setdefault(data["stage"], []).append(node)

    positions = {}
    for stage, nodes in stages.items():
        nodes.sort()
        for row, node in enumerate(nodes):
            positions[node] = {"x": stage, "y": row}
    return positions


def graph_to_json(graph, paths, labels):
    positions = layout_by_stage(graph)
    nodes = [{"name": n, "x": positions[n]["x"], "y": positions[n]["y"]} for n in graph.nodes()]
    edges = [{"from": u, "to": v} for u, v in graph.edges()]
    return {"nodes": nodes, "edges": edges, "paths": paths, "labels": labels}


def export_baseline():
    n = 8
    graph = build_baseline_network(n)
    paths = {}
    for source in range(n):
        for destination in range(n):
            key = f"{source}->{destination}"
            paths[key] = route_baseline(source, destination, n)
    labels = {str(i): f"in {i}" for i in range(n)}
    return graph_to_json(graph, paths, labels)


def export_benes():
    n = 8
    graph = build_benes_network(n)
    # a single connection has no other traffic to clash with, so any
    # forward path through the graph works — no need for the full
    # Looping Algorithm, which is for routing many connections at once
    paths = {}
    for source in range(n):
        for destination in range(n):
            key = f"{source}->{destination}"
            path = nx.shortest_path(graph, f"s0_{source // 2}", f"s4_{destination // 2}")
            paths[key] = path
    labels = {str(i): f"in {i}" for i in range(n)}
    return graph_to_json(graph, paths, labels)


def export_clos():
    r, n, m = 4, 3, 5
    graph = build_clos_network(r, n, m)
    total_inputs = r * n
    paths = {}
    for source in range(total_inputs):
        for destination in range(total_inputs):
            key = f"{source}->{destination}"
            paths[key] = route_clos(source, destination, r, n, m)
    labels = {str(i): f"in {i}" for i in range(total_inputs)}
    return graph_to_json(graph, paths, labels)


def export_xgft():
    h, m, w = 2, 2, 2
    graph = build_xgft_network(h, m, w)
    num_leaves = m ** h
    paths = {}
    for source in range(num_leaves):
        for destination in range(num_leaves):
            if source == destination:
                continue
            key = f"{source}->{destination}"
            paths[key] = route_xgft(source, destination, h, m, w)
    labels = {str(i): f"leaf {i}" for i in range(num_leaves)}
    return graph_to_json(graph, paths, labels)


if __name__ == "__main__":
    data = {
        "baseline": export_baseline(),
        "benes": export_benes(),
        "clos": export_clos(),
        "xgft": export_xgft(),
    }
    with open("demo_data.json", "w") as f:
        json.dump(data, f)
    print("saved demo_data.json")
    for name, net in data.items():
        print(f"{name}: {len(net['nodes'])} nodes, {len(net['edges'])} edges, {len(net['paths'])} paths")
