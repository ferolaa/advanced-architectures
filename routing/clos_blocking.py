"""
Blocking detection for the Clos network.

A middle switch is "busy" for an input switch once one of that
input switch's calls is using it, and busy for an output switch the
same way. A new call from input switch i to output switch j can
only use a middle switch that is free on both sides. If none is
free, the call is blocked, even though a physical path exists.
"""

import random


class ClosCallState:
    """Tracks which middle switches are busy for each input and output switch."""

    def __init__(self, r, m):
        self.m = m
        self.busy_at_input = [set() for _ in range(r)]
        self.busy_at_output = [set() for _ in range(r)]

    def attempt_call(self, in_switch, out_switch):
        """
        Tries to route one call from in_switch to out_switch.
        Returns the middle switch used, or None if blocked.
        """
        for mid in range(self.m):
            if mid not in self.busy_at_input[in_switch] and mid not in self.busy_at_output[out_switch]:
                self.busy_at_input[in_switch].add(mid)
                self.busy_at_output[out_switch].add(mid)
                return mid
        return None


def simulate_random_traffic(r, n, m, seed=None):
    """
    Fills up a Clos network (r input/output switches, n ports each,
    m middle switches) with random calls, respecting the n-port
    limit per switch. Returns the number of calls that were blocked.
    """
    if seed is not None:
        random.seed(seed)

    state = ClosCallState(r, m)
    blocked_count = 0

    # each input switch makes n calls, to random output switches
    # that still have a free port
    output_remaining = [n] * r
    for in_switch in range(r):
        available_outputs = [j for j in range(r) if output_remaining[j] > 0]
        random.shuffle(available_outputs)
        chosen_outputs = available_outputs[:n]
        for out_switch in chosen_outputs:
            output_remaining[out_switch] -= 1
            result = state.attempt_call(in_switch, out_switch)
            if result is None:
                blocked_count += 1

    return blocked_count


if __name__ == "__main__":
    # manual check: a small network, one random traffic pattern
    r, n, m = 6, 4, 4
    blocked = simulate_random_traffic(r, n, m, seed=1)
    print(f"r={r}, n={n}, m={m}: {blocked} calls blocked")
