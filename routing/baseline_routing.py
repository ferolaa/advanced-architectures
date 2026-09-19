"""
Self-routing for the Baseline network.

Rule: at each stage, if the destination's bit for that stage is 0,
the path goes "straight". If it is 1, it "crosses".
"""

import math


def route_baseline(source, destination, n):
    """
    Finds the path from an input to an output in a Baseline network
    with n inputs. Returns a list of switch names, one per stage.
    """
    if n < 2 or (n & (n - 1)) != 0:
        raise ValueError("n must be a power of 2, like 2, 4, 8, 16...")
    if not (0 <= source < n) or not (0 <= destination < n):
        raise ValueError("source and destination must be between 0 and n-1")

    num_stages = int(math.log2(n))

    # two inputs share one switch at stage 0
    switch_id = source // 2
    path = [f"s0_{switch_id}"]

    # one destination bit examined per stage
    for stage in range(num_stages - 1):
        bit_position = num_stages - 2 - stage
        destination_bit = (destination >> bit_position) & 1

        # bit set to match destination: straight if already matching, cross otherwise
        switch_id = (switch_id & ~(1 << bit_position)) | (destination_bit << bit_position)
        path.append(f"s{stage + 1}_{switch_id}")

    return path


if __name__ == "__main__":
    # manual check
    n = 8
    for source in range(n):
        for destination in range(n):
            path = route_baseline(source, destination, n)
            print(f"input {source} -> output {destination}: {path}")
