"""
Demo: sends a batch of traffic through each network and prints the
paths taken. Shows all four networks and their routing working
together.
"""

import random

from networks.baseline import build_baseline_network
from networks.benes import build_benes_network
from networks.clos import build_clos_network
from networks.xgft import build_xgft_network
from routing.baseline_routing import route_baseline
from routing.benes_routing import route_benes_permutation
from routing.clos_routing import route_clos
from routing.xgft_routing import route_xgft


def demo_baseline(n, num_requests):
    print(f"\n--- Baseline network, n={n} ---")
    build_baseline_network(n)  # network built, not printed here
    for _ in range(num_requests):
        source = random.randrange(n)
        destination = random.randrange(n)
        path = route_baseline(source, destination, n)
        print(f"input {source} -> output {destination}: {path}")


def demo_benes(n):
    print(f"\n--- Benes network, n={n} ---")
    build_benes_network(n)  # network built, not printed here
    perm = list(range(n))
    random.shuffle(perm)
    settings = route_benes_permutation(perm)
    print(f"permutation: {perm}")
    print(f"switch settings: {settings}")


def demo_clos(r, n, m, num_requests):
    print(f"\n--- Clos network, r={r}, n={n}, m={m} ---")
    build_clos_network(r, n, m)  # network built, not printed here
    total_inputs = r * n
    for _ in range(num_requests):
        source = random.randrange(total_inputs)
        destination = random.randrange(total_inputs)
        path = route_clos(source, destination, r, n, m)
        print(f"input {source} -> output {destination}: {path}")


def demo_xgft(h, m, w, num_requests):
    print(f"\n--- XGFT fat-tree, h={h}, m={m}, w={w} ---")
    build_xgft_network(h, m, w)  # network built, not printed here
    num_leaves = m ** h
    for _ in range(num_requests):
        source = random.randrange(num_leaves)
        destination = random.randrange(num_leaves)
        if source == destination:
            continue
        path = route_xgft(source, destination, h, m, w)
        print(f"leaf {source} -> leaf {destination}: {path}")


if __name__ == "__main__":
    demo_baseline(n=8, num_requests=5)
    demo_benes(n=8)
    demo_clos(r=4, n=3, m=5, num_requests=5)
    demo_xgft(h=2, m=2, w=2, num_requests=5)
