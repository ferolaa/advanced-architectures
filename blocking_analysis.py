"""
Shows how often calls get blocked in a Clos network, as the number
of middle switches (m) changes. Many random traffic patterns are
tried for each m, and the average blocking rate is plotted.

Clos's theorem says m >= 2n - 1 middle switches guarantee no
blocking, no matter the traffic. This is checked directly: the
blocking rate should hit zero exactly at that point.
"""

import matplotlib.pyplot as plt

from routing.clos_blocking import simulate_random_traffic


def measure_blocking_rate(r, n, m, num_trials=300):
    """Average fraction of calls blocked, across num_trials random traffic patterns."""
    total_calls = r * n
    total_blocked = 0
    for trial in range(num_trials):
        total_blocked += simulate_random_traffic(r, n, m, seed=trial)
    return total_blocked / (total_calls * num_trials)


def measure_blocking_by_m(r, n, m_values, num_trials=300):
    """Blocking rate for each m in m_values."""
    rates = []
    for m in m_values:
        rates.append(measure_blocking_rate(r, n, m, num_trials))
    return rates


def plot_blocking(m_values, rates, threshold, filename):
    plt.figure(figsize=(7, 5))
    plt.plot(m_values, rates, marker="o", label="Measured blocking rate")
    plt.axvline(threshold, color="red", linestyle="--", label=f"Non-blocking threshold (m={threshold})")
    plt.xlabel("Middle switches (m)")
    plt.ylabel("Fraction of calls blocked")
    plt.title("Clos network blocking rate vs middle switch count")
    plt.legend()
    plt.savefig(filename, bbox_inches="tight")
    plt.close()
    print(f"saved {filename}")


if __name__ == "__main__":
    r, n = 8, 5
    threshold = 2 * n - 1
    m_values = list(range(2, threshold + 3))

    rates = measure_blocking_by_m(r, n, m_values)
    for m, rate in zip(m_values, rates):
        print(f"m={m}: blocking rate = {rate:.3f}")

    plot_blocking(m_values, rates, threshold, "pictures/blocking_rate.png")
