"""
Checks Clos's non-blocking guarantee directly: at m = 2n - 1 or
above, no random permutation should ever get blocked. Also checks
that the blocking detector is not trivially broken, by confirming
blocking does happen sometimes when m is small.
"""

from routing.clos_blocking import simulate_random_traffic


def check_non_blocking_guarantee(r, n, trials=500):
    """At m = 2n - 1, no trial should show any blocked call."""
    m = 2 * n - 1
    total_blocked = 0
    for seed in range(trials):
        total_blocked += simulate_random_traffic(r, n, m, seed=seed)
    if total_blocked == 0:
        print(f"r={r}, n={n}, m={m} (threshold): 0 blocked calls in {trials} trials, as expected.")
    else:
        print(f"PROBLEM: r={r}, n={n}, m={m} (threshold) had {total_blocked} blocked calls, expected 0.")


def check_blocking_can_happen(r, n, small_m, trials=100):
    """With a small m, at least some blocking should show up, or the detector may be broken."""
    total_blocked = 0
    for seed in range(trials):
        total_blocked += simulate_random_traffic(r, n, small_m, seed=seed)
    if total_blocked > 0:
        print(f"r={r}, n={n}, m={small_m} (small): {total_blocked} blocked calls in {trials} trials, as expected.")
    else:
        print(f"PROBLEM: r={r}, n={n}, m={small_m} (small) had 0 blocked calls — check the detector.")


if __name__ == "__main__":
    check_non_blocking_guarantee(r=8, n=5)
    check_non_blocking_guarantee(r=6, n=3)
    check_blocking_can_happen(r=8, n=5, small_m=2)
