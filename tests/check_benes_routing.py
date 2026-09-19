"""
Checks that the switch settings from the Looping Algorithm really
reproduce the permutation they were built for.

Works by simulating data flowing through the settings: at each
stage, "straight" or "cross" decides where each input goes, and the
final output positions are compared against the original permutation.
"""

import random

from routing.benes_routing import route_benes_permutation


def simulate_benes(settings, n):
    """Simulates the network given its switch settings, for n inputs."""
    if n == 2:
        setting = settings["first_stage"][0]
        return [0, 1] if setting == "straight" else [1, 0]

    half = n // 2
    first_stage = settings["first_stage"]
    last_stage = settings["last_stage"]
    top_result = simulate_benes(settings["top"], half)
    bottom_result = simulate_benes(settings["bottom"], half)

    output = [0] * n
    for i in range(half):
        for port in (0, 1):
            goes_top = (port == 0) == (first_stage[i] == "straight")
            sub_result = top_result if goes_top else bottom_result
            out_switch = sub_result[i]
            port_matches_top = (last_stage[out_switch] == "straight") == goes_top
            out_port = 0 if port_matches_top else 1
            output[2 * i + port] = 2 * out_switch + out_port

    return output


def check_random_permutations(n, count=20):
    """Tries several random permutations and checks the settings work."""
    mistakes = 0
    for _ in range(count):
        perm = list(range(n))
        random.shuffle(perm)
        settings = route_benes_permutation(perm)
        result = simulate_benes(settings, n)
        if result != perm:
            print(f"PROBLEM: expected {perm}, got {result}")
            mistakes += 1
    if mistakes == 0:
        print(f"All {count} random permutations for n={n} were correct!")
    else:
        print(f"Found {mistakes} problems for n={n}.")


if __name__ == "__main__":
    check_random_permutations(4)
    check_random_permutations(8)
    check_random_permutations(16)
