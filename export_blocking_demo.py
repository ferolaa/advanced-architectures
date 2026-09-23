"""
Builds two Clos networks (same r and n, different m) and traces the
exact same random traffic through both, step by step. Written out
as JSON for the "blocking, live" animation.
"""

import json
import random

from networks.clos import build_clos_network
from routing.clos_blocking import trace_permutation
from export_demo_data import layout_by_stage


def export_side(r, n, m, perm):
    graph = build_clos_network(r, n, m)
    positions = layout_by_stage(graph)
    nodes = [{"name": name, "x": positions[name]["x"], "y": positions[name]["y"]} for name in graph.nodes()]
    edges = [{"from": u, "to": v} for u, v in graph.edges()]
    steps = trace_permutation(r, n, m, perm)
    return {"m": m, "nodes": nodes, "edges": edges, "steps": steps}


if __name__ == "__main__":
    r, n = 4, 3
    threshold = 2 * n - 1
    small_m = 2

    random.seed(0)
    perm = list(range(r * n))
    random.shuffle(perm)

    data = {
        "r": r,
        "n": n,
        "small": export_side(r, n, small_m, perm),
        "threshold": export_side(r, n, threshold, perm),
    }

    blocked_small = sum(1 for s in data["small"]["steps"] if s["middle"] is None)
    blocked_threshold = sum(1 for s in data["threshold"]["steps"] if s["middle"] is None)
    print(f"small m={small_m}: {blocked_small} blocked out of {r * n}")
    print(f"threshold m={threshold}: {blocked_threshold} blocked out of {r * n}")

    with open("blocking_demo_data.json", "w") as f:
        json.dump(data, f)
    print("saved blocking_demo_data.json")
