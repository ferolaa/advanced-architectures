"""
Checks whether a Clos network can route a full permutation without
blocking, for different numbers of middle switches (m).

A connection from input switch i to output switch k needs a middle
switch that is free on both the i-side link and the k-side link.
Each switch link can carry only one connection at a time.

Theory says: if m >= 2n - 1 (n = inputs per switch), a Clos network
is strictly non-blocking — every permutation can be routed, in any
order, using a simple first-fit search for a free middle switch.
Below that, blocking can happen.
"""

import random
import matplotlib.pyplot as plt


def try_route_permutation(r, n, m, perm):
    """
    Tries to route a full permutation through a Clos network
    (r input/output switches, n inputs each, m middle switches).
    Returns True if every connection found a free middle switch.
    """
    input_busy = [set() for _ in range(r)]
    output_busy = [set() for _ in range(r)]

    for source in range(r * n):
        in_switch = source // n
        out_switch = perm[source] // n

        chosen = None
        for mid in range(m):
            if mid not in input_busy[in_switch] and mid not in output_busy[out_switch]:
                chosen = mid
                break

        if chosen is None:
            return False  # blocked: no free middle switch for this connection

        input_busy[in_switch].add(chosen)
        output_busy[out_switch].add(chosen)

    return True


def success_rate(r, n, m, trials=200):
    """Tries several random permutations and returns the fraction routed successfully."""
    successes = 0
    for _ in range(trials):
        perm = list(range(r * n))
        random.shuffle(perm)
        if try_route_permutation(r, n, m, perm):
            successes += 1
    return successes / trials


def plot_success_rates(r, n, m_values, rates, threshold, filename):
    plt.figure(figsize=(7, 5))
    plt.plot(m_values, [rate * 100 for rate in rates], marker="o")
    plt.axvline(threshold, color="red", linestyle="--", label=f"non-blocking threshold (m={threshold})")
    plt.xlabel("Middle switches (m)")
    plt.ylabel("Routing success rate (%)")
    plt.title(f"Clos blocking vs middle switch count (r={r}, n={n})")
    plt.legend()
    plt.savefig(filename, bbox_inches="tight")
    plt.close()
    print(f"saved {filename}")


if __name__ == "__main__":
    r, n = 6, 4
    threshold = 2 * n - 1
    print(f"r={r}, n={n}, non-blocking threshold m >= {threshold}")

    m_values = [3, 4, 5, 6, threshold, threshold + 2]
    rates = []
    for m in m_values:
        rate = success_rate(r, n, m, trials=200)
        rates.append(rate)
        print(f"m={m}: success rate = {rate * 100:.1f}%")

    # note: below the threshold, blocking CAN happen but does not have to
    # for every permutation — the guarantee only kicks in at m >= 2n-1
    plot_success_rates(r, n, m_values, rates, threshold, "pictures/blocking_vs_m.png")

