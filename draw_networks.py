"""
Draws each network as a picture and saves it in the pictures folder.

Switches are placed left to right by stage, and stacked top to
bottom within a stage, so the wires between stages are easy to see.
"""

import matplotlib.pyplot as plt
import networkx as nx

from networks.baseline import build_baseline_network
from networks.benes import build_benes_network
from networks.clos import build_clos_network
from networks.xgft import build_xgft_network


def draw_network(graph, title, filename):
    """Draws a graph with switches grouped by stage, and saves it as a PNG."""
    stages = {}
    for node, data in graph.nodes(data=True):
        stages.setdefault(data["stage"], []).append(node)

    positions = {}
    for stage, nodes in stages.items():
        nodes.sort()
        for row, node in enumerate(nodes):
            positions[node] = (stage, -row)

    plt.figure(figsize=(8, 6))
    nx.draw(
        graph,
        pos=positions,
        with_labels=True,
        node_size=800,
        node_color="lightblue",
        font_size=7,
        arrows=True,
    )
    plt.title(title)
    plt.savefig(filename, bbox_inches="tight")
    plt.close()
    print(f"saved {filename}")


if __name__ == "__main__":
    baseline_net = build_baseline_network(8)
    draw_network(baseline_net, "Baseline network (n=8)", "pictures/baseline.png")

    benes_net = build_benes_network(8)
    draw_network(benes_net, "Benes network (n=8)", "pictures/benes.png")

    clos_net = build_clos_network(4, 3, 5)
    draw_network(clos_net, "Clos network (r=4, n=3, m=5)", "pictures/clos.png")

    xgft_net = build_xgft_network(h=2, m=2, w=2)
    draw_network(xgft_net, "XGFT fat-tree (h=2, m=2, w=2)", "pictures/xgft.png")
