"""
Baseline network builder (also called a Butterfly network).

N inputs are connected to N outputs through small 2x2 switches
arranged in stages. N must be a power of 2.
"""

import networkx as nx
import math


def build_baseline_network(n):
    """
    Builds a Baseline network for n inputs (n must be a power of 2).
    Switches are named "s<stage>_<id>".
    """
    if n < 2 or (n & (n - 1)) != 0:
        raise ValueError("n must be a power of 2, like 2, 4, 8, 16...")

    num_stages = int(math.log2(n))
    num_switches_per_stage = n // 2

    graph = nx.DiGraph()

    # switches added stage by stage
    for stage in range(num_stages):
        for switch_id in range(num_switches_per_stage):
            graph.add_node(f"s{stage}_{switch_id}", stage=stage)

    # stages connected to each other
    for stage in range(num_stages - 1):
        for switch_id in range(num_switches_per_stage):
            next_a, next_b = _baseline_targets(switch_id, stage, num_switches_per_stage)
            graph.add_edge(f"s{stage}_{switch_id}", f"s{stage + 1}_{next_a}")
            graph.add_edge(f"s{stage}_{switch_id}", f"s{stage + 1}_{next_b}")

    return graph


def _baseline_targets(switch_id, stage, num_switches_per_stage):
    """Standard Baseline bit-flip rule for the next stage's targets."""
    bit_to_flip = num_switches_per_stage // (2 ** stage) // 2
    if bit_to_flip == 0:
        bit_to_flip = 1
    partner = switch_id ^ bit_to_flip
    return switch_id, partner


if __name__ == "__main__":
    # manual check
    net = build_baseline_network(8)
    print("Switches:", list(net.nodes(data=True)))
    print("Wires:", list(net.edges()))
