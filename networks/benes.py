"""
Benes network builder.

Made of two Baseline networks placed back to back, sharing one
middle stage. Any input can be connected to any output with no
clashes, given the right routing.

Number of stages for n inputs: 2 * log2(n) - 1.
"""

import networkx as nx
import math

from networks.baseline import build_baseline_network


def build_benes_network(n):
    """
    Builds a Benes network for n inputs (n must be a power of 2).
    A Baseline network is mirrored after the middle stage.
    """
    if n < 2 or (n & (n - 1)) != 0:
        raise ValueError("n must be a power of 2, like 2, 4, 8, 16...")

    num_baseline_stages = int(math.log2(n))
    num_switches_per_stage = n // 2

    # first half: a normal Baseline network
    forward_part = build_baseline_network(n)

    graph = nx.DiGraph()
    graph.add_nodes_from(forward_part.nodes(data=True))
    graph.add_edges_from(forward_part.edges())

    middle_stage = num_baseline_stages - 1
    total_stages = 2 * num_baseline_stages - 1

    # mirrored switches labeled
    for stage in range(middle_stage + 1, total_stages):
        for switch_id in range(num_switches_per_stage):
            graph.add_node(f"s{stage}_{switch_id}", stage=stage)

    # mirrored part connected, same bit-flip rule in reverse
    for stage in range(middle_stage, total_stages - 1):
        for switch_id in range(num_switches_per_stage):
            bit_to_flip = num_switches_per_stage // (2 ** (total_stages - 2 - stage)) // 2
            if bit_to_flip == 0:
                bit_to_flip = 1
            partner = switch_id ^ bit_to_flip
            graph.add_edge(f"s{stage}_{switch_id}", f"s{stage + 1}_{switch_id}")
            graph.add_edge(f"s{stage}_{switch_id}", f"s{stage + 1}_{partner}")

    return graph


if __name__ == "__main__":
    # manual check
    net = build_benes_network(8)
    stages_used = sorted(set(data["stage"] for _, data in net.nodes(data=True)))
    print("Number of stages:", len(stages_used))
    print("Number of switches:", net.number_of_nodes())
    print("Number of wires:", net.number_of_edges())
