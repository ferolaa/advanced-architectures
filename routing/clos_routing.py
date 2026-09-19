"""
Simple routing for the Clos network.

Every input switch is connected to every middle switch, and every
middle switch is connected to every output switch, so any middle
switch can be used to connect any input to any output. One middle
switch is picked using a simple rule, spreading traffic across them.
"""


def route_clos(source, destination, r, n, m):
    """
    Finds a path from an input to an output in a Clos network.
    r = input/output switches, n = inputs per input switch, m = middle switches.

    Returns a list of three switch names: input, middle, output.
    """
    total_inputs = r * n
    if not (0 <= source < total_inputs) or not (0 <= destination < total_inputs):
        raise ValueError("source and destination must be between 0 and r*n - 1")

    in_switch = source // n
    out_switch = destination // n

    # middle switch picked with a simple rule, to spread traffic out
    mid_switch = (in_switch + out_switch) % m

    return [f"in_{in_switch}", f"mid_{mid_switch}", f"out_{out_switch}"]


if __name__ == "__main__":
    # manual check
    r, n, m = 4, 3, 5
    for source in range(0, r * n, 4):
        for destination in range(0, r * n, 5):
            print(source, "->", destination, ":", route_clos(source, destination, r, n, m))
