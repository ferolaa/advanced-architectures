"""
Looks at how the size of each network grows as the number of
inputs grows. Switch count and wire count are measured for a range
of sizes, and plotted.
"""

import matplotlib.pyplot as plt

from networks.baseline import build_baseline_network
from networks.benes import build_benes_network
from networks.clos import build_clos_network
from networks.xgft import build_xgft_network


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


def measure_clos_by_m(m_values, r=8, n=4):
    """
    Returns switch and wire counts for a fixed-size Clos network
    (r input/output switches, n inputs each), as m (middle switch
    count) varies. Shows the cost of adding redundant middle paths.
    """
    switches = []
    wires = []
    for m in m_values:
        clos_net = build_clos_network(r, n, m)
        switches.append(clos_net.number_of_nodes())
        wires.append(clos_net.number_of_edges())
    return {"m_values": m_values, "switches": switches, "wires": wires}


def plot_clos_by_m(clos_by_m, filename):
    plt.figure(figsize=(7, 5))
    plt.plot(clos_by_m["m_values"], clos_by_m["switches"], marker="o", label="Total switches")
    plt.plot(clos_by_m["m_values"], clos_by_m["wires"], marker="o", label="Total wires")
    plt.xlabel("Middle switches (m)")
    plt.ylabel("Count")
    plt.title("Clos network cost vs middle switch count (fixed size)")
    plt.legend()
    plt.savefig(filename, bbox_inches="tight")
    plt.close()
    print(f"saved {filename}")


def measure_all_topologies(sizes):
    """
    Returns switch counts for all four topologies, for each N in
    sizes. N must be a power of 4, so it works as both a power of 2
    (for Baseline/Benes) and a perfect square (for Clos/XGFT).

    Baseline, Benes and XGFT (with w=2) are all non-blocking or
    close to it by construction. To keep the comparison fair, Clos
    uses m = 2*side - 1, the proven minimum for non-blocking (see
    REPORT.md) — not the cheapest possible, blocking, setup.
    """
    results = {"baseline": [], "benes": [], "clos": [], "xgft": []}
    for n in sizes:
        side = int(round(n ** 0.5))

        baseline_net = build_baseline_network(n)
        results["baseline"].append(baseline_net.number_of_nodes())

        benes_net = build_benes_network(n)
        results["benes"].append(benes_net.number_of_nodes())

        clos_net = build_clos_network(r=side, n=side, m=2 * side - 1)
        results["clos"].append(clos_net.number_of_nodes())

        xgft_net = build_xgft_network(h=2, m=side, w=2)
        results["xgft"].append(xgft_net.number_of_nodes())

    return results


def plot_all_topologies(sizes, results, filename):
    plt.figure(figsize=(7, 5))
    for name in ["baseline", "benes", "clos", "xgft"]:
        plt.plot(sizes, results[name], marker="o", label=name)
    plt.xlabel("Number of inputs (N)")
    plt.ylabel("Total switches")
    plt.title("Switch count vs network size, all topologies")
    plt.legend()
    plt.savefig(filename, bbox_inches="tight")
    plt.close()
    print(f"saved {filename}")


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

    m_values = [2, 4, 6, 8, 10, 12, 16]
    clos_by_m = measure_clos_by_m(m_values, r=8, n=4)
    for m, sw, wi in zip(clos_by_m["m_values"], clos_by_m["switches"], clos_by_m["wires"]):
        print(f"m={m}: switches={sw}, wires={wi}")
    plot_clos_by_m(clos_by_m, "pictures/scaling_clos_by_m.png")

    all_sizes = [4, 16, 64, 256]
    all_results = measure_all_topologies(all_sizes)
    for i, n in enumerate(all_sizes):
        print(f"N={n}: baseline={all_results['baseline'][i]}, benes={all_results['benes'][i]}, "
              f"clos={all_results['clos'][i]}, xgft={all_results['xgft'][i]}")
    plot_all_topologies(all_sizes, all_results, "pictures/scaling_all_topologies.png")
