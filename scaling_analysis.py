"""
Looks at how the size of each network grows as the number of
inputs grows. Switch count and wire count are measured for a range
of sizes, and plotted.
"""

import matplotlib.pyplot as plt

from networks.baseline import build_baseline_network
from networks.benes import build_benes_network
from networks.clos import build_clos_network


def measure_baseline_and_benes(sizes):
    """Returns switch and wire counts for both networks, for each size in sizes."""
    results = {"baseline_switches": [], "baseline_wires": [], "benes_switches": [], "benes_wires": []}
    for n in sizes:
        baseline_net = build_baseline_network(n)
        results["baseline_switches"].append(baseline_net.number_of_nodes())
        results["baseline_wires"].append(baseline_net.number_of_edges())

        benes_net = build_benes_network(n)
        results["benes_switches"].append(benes_net.number_of_nodes())
        results["benes_wires"].append(benes_net.number_of_edges())
    return results


def measure_clos(sizes, n_per_switch=4, m=6):
    """Returns switch and wire counts for a Clos network, for each r in sizes."""
    switches = []
    wires = []
    total_inputs = []
    for r in sizes:
        clos_net = build_clos_network(r, n_per_switch, m)
        switches.append(clos_net.number_of_nodes())
        wires.append(clos_net.number_of_edges())
        total_inputs.append(r * n_per_switch)
    return {"total_inputs": total_inputs, "switches": switches, "wires": wires}


def plot_baseline_and_benes(sizes, results, filename):
    plt.figure(figsize=(7, 5))
    plt.plot(sizes, results["baseline_switches"], marker="o", label="Baseline switches")
    plt.plot(sizes, results["benes_switches"], marker="o", label="Benes switches")
    plt.xlabel("Number of inputs (N)")
    plt.ylabel("Number of switches")
    plt.title("Switch count vs network size")
    plt.legend()
    plt.savefig(filename, bbox_inches="tight")
    plt.close()
    print(f"saved {filename}")


def plot_clos(clos_results, filename):
    plt.figure(figsize=(7, 5))
    plt.plot(clos_results["total_inputs"], clos_results["switches"], marker="o", label="Clos switches")
    plt.plot(clos_results["total_inputs"], clos_results["wires"], marker="o", label="Clos wires")
    plt.xlabel("Number of inputs")
    plt.ylabel("Count")
    plt.title("Clos network size vs number of inputs")
    plt.legend()
    plt.savefig(filename, bbox_inches="tight")
    plt.close()
    print(f"saved {filename}")


if __name__ == "__main__":
    sizes = [2, 4, 8, 16, 32, 64]
    results = measure_baseline_and_benes(sizes)
    for n, bs, bw, ns, nw in zip(
        sizes, results["baseline_switches"], results["baseline_wires"],
        results["benes_switches"], results["benes_wires"]
    ):
        print(f"N={n}: baseline switches={bs}, wires={bw} | benes switches={ns}, wires={nw}")
    plot_baseline_and_benes(sizes, results, "pictures/scaling_baseline_benes.png")

    clos_sizes = [2, 4, 8, 16, 32]
    clos_results = measure_clos(clos_sizes)
    for total, sw, wi in zip(clos_results["total_inputs"], clos_results["switches"], clos_results["wires"]):
        print(f"total inputs={total}: switches={sw}, wires={wi}")
    plot_clos(clos_results, "pictures/scaling_clos.png")
