"""
Blocking detection for the Clos network.

A middle switch is "busy" for an input switch once one of that
input switch's calls is using it, and busy for an output switch the
same way. A new call from input switch i to output switch j can
only use a middle switch that is free on both sides. If none is
free, the call is blocked, even though a physical path exists.

Traffic is generated as a full permutation (every one of the r*n
inputs sent to a distinct output). This guarantees every input
switch sends exactly n calls and every output switch receives
exactly n calls, matching the n ports each switch actually has, and
matches how Clos's theorem itself is usually stated (in terms of
permutations).
"""

import random


def try_route_permutation(r, n, m, perm):
    """
    Tries to route a full permutation through a Clos network
    (r input/output switches, n inputs each, m middle switches).
    Returns the number of calls that were blocked.
    """
    input_busy = [set() for _ in range(r)]
    output_busy = [set() for _ in range(r)]
    blocked_count = 0

    for source in range(r * n):
        in_switch = source // n
        out_switch = perm[source] // n

        chosen = None
        for mid in range(m):
            if mid not in input_busy[in_switch] and mid not in output_busy[out_switch]:
                chosen = mid
                break

        if chosen is None:
            blocked_count += 1
            continue

        input_busy[in_switch].add(chosen)
        output_busy[out_switch].add(chosen)

    return blocked_count


def simulate_random_traffic(r, n, m, seed=None):
    """
    Builds one random permutation of the r*n inputs and routes it.
    Returns the number of calls that were blocked.
    """
    if seed is not None:
        random.seed(seed)
    perm = list(range(r * n))
    random.shuffle(perm)
    return try_route_permutation(r, n, m, perm)


if __name__ == "__main__":
    # manual check: a small network, one random traffic pattern
    r, n, m = 6, 4, 4
    blocked = simulate_random_traffic(r, n, m, seed=1)
    print(f"r={r}, n={n}, m={m}: {blocked} calls blocked")
