"""
I build a Baseline network here (also called a Butterfly network).

A Baseline network connects N inputs to N outputs using small 2x2 switches,
arranged in stages. N must be a power of 2 (like 4, 8, 16...).

Example: with N = 8 inputs, I need log2(8) = 3 stages of switches.
Each stage has N/2 = 4 switches.

I use a graph (from the networkx library) to store the network.
Each switch is a "node" in the graph.
Each wire between switches is an "edge" in the graph.
"""

import networkx as nx
import math


def build_baseline_network(n):
    """
    I build a Baseline network for n inputs (n must be a power of 2).

    I return a networkx graph. Each switch is named like "s1_2"
    meaning "stage 1, switch 2".
    """
    if n < 2 or (n & (n - 1)) != 0:
        raise ValueError("n must be a power of 2, like 2, 4, 8, 16...")

    num_stages = int(math.log2(n))
    num_switches_per_stage = n // 2

    graph = nx.DiGraph()  # DiGraph = directed graph, wires only go one way

    # I add all switches first, one row per stage
    for stage in range(num_stages):
        for switch_id in range(num_switches_per_stage):
            graph.add_node(f"s{stage}_{switch_id}", stage=stage)

    # now I connect each stage to the next one
    for stage in range(num_stages - 1):
        for switch_id in range(num_switches_per_stage):
            # each switch has 2 outputs, going to 2 switches in the next stage
            next_a, next_b = _baseline_targets(switch_id, stage, num_switches_per_stage)
            graph.add_edge(f"s{stage}_{switch_id}", f"s{stage + 1}_{next_a}")
            graph.add_edge(f"s{stage}_{switch_id}", f"s{stage + 1}_{next_b}")

    return graph


def _baseline_targets(switch_id, stage, num_switches_per_stage):
    """
    I work out which two switches in the next stage this switch connects to.

    At each stage, I flip one bit of the switch number to find the
    two possible next switches. This is the standard Baseline rule.
    """
    bit_to_flip = num_switches_per_stage // (2 ** stage) // 2
    if bit_to_flip == 0:
        bit_to_flip = 1
    partner = switch_id ^ bit_to_flip
    return switch_id, partner


if __name__ == "__main__":
    # I do a quick manual check here: build a small network and print it out
    net = build_baseline_network(8)
    print("Switches:", list(net.nodes(data=True)))
    print("Wires:", list(net.edges()))
