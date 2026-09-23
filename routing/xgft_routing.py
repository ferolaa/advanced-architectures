"""
Routing for the XGFT fat-tree.

The path goes up from the source leaf until reaching the lowest
level where the source and destination share the same "logical
position" (their common ancestor), then goes back down to the
destination leaf. The first available switch copy is used at every
step.
"""


def route_xgft(source, destination, h, m, w):
    """
    Finds a path from a source leaf to a destination leaf in an
    XGFT fat-tree with height h, branching factor m, redundancy w.
    Returns a list of node names.
    """
    num_leaves = m ** h
    if not (0 <= source < num_leaves) or not (0 <= destination < num_leaves):
        raise ValueError("source and destination must be between 0 and m^h - 1")

    if source == destination:
        return [f"leaf_{source}"]

    # lowest level where source and destination share a position
    level = 0
    while source // (m ** level) != destination // (m ** level):
        level += 1

    path = [f"leaf_{source}"]
    for i in range(1, level + 1):
        position = source // (m ** i)
        path.append(f"L{i}_{position}_0")

    for i in range(level - 1, 0, -1):
        position = destination // (m ** i)
        path.append(f"L{i}_{position}_0")
    path.append(f"leaf_{destination}")

    return path


if __name__ == "__main__":
    # manual check
    h, m, w = 2, 2, 2
    for source in range(m ** h):
        for destination in range(m ** h):
            print(f"leaf {source} -> leaf {destination}: {route_xgft(source, destination, h, m, w)}")
