"""
Looping Algorithm for the Benes network.

Given a permutation (a full input-to-output mapping), the setting
of every switch (straight or cross) is worked out so the whole
permutation is routed with no clashes.

A Benes network of size n is split into a first stage of n/2
switches, two half-size Benes networks in the middle, and a last
stage of n/2 switches. The algorithm assigns each connection to the
top or bottom half-network, then recurses on each half.
"""


def route_benes_permutation(perm):
    """
    Works out switch settings for a full permutation.
    perm[i] = output index reached from input i. len(perm) must be a power of 2.

    Returns a nested dict:
    - "first_stage": list of "straight"/"cross" settings, one per switch
    - "last_stage": same, for the last stage
    - "top", "bottom": same structure, for the two half-size sub-networks
    Base case (n == 2) only has "first_stage".
    """
    n = len(perm)
    if n == 1:
        return {}
    if n == 2:
        setting = "straight" if perm[0] == 0 else "cross"
        return {"first_stage": [setting]}

    half = n // 2
    edges = _build_edges(perm, half)
    color = _color_edges(edges, half)

    first_stage = []
    last_stage = []
    perm_top = [0] * half
    perm_bottom = [0] * half

    edge_by_in = {(e["in_switch"], e["in_port"]): e for e in edges}
    edge_by_out = {(e["out_switch"], e["out_port"]): e for e in edges}

    for i in range(half):
        top_color = color[edge_by_in[(i, 0)]["id"]]
        first_stage.append("straight" if top_color == 0 else "cross")
        perm_top[i] = edge_by_in[(i, 0)]["out_switch"] if top_color == 0 else edge_by_in[(i, 1)]["out_switch"]
        perm_bottom[i] = edge_by_in[(i, 1)]["out_switch"] if top_color == 0 else edge_by_in[(i, 0)]["out_switch"]

    for j in range(half):
        top_color = color[edge_by_out[(j, 0)]["id"]]
        last_stage.append("straight" if top_color == 0 else "cross")

    return {
        "first_stage": first_stage,
        "last_stage": last_stage,
        "top": route_benes_permutation(perm_top),
        "bottom": route_benes_permutation(perm_bottom),
    }


def _build_edges(perm, half):
    """One edge per input, linking its input switch/port to its output switch/port."""
    edges = []
    for i in range(half):
        for port in (0, 1):
            idx = 2 * i + port
            dest = perm[idx]
            edges.append({
                "id": idx,
                "in_switch": i,
                "in_port": port,
                "out_switch": dest // 2,
                "out_port": dest % 2,
            })
    return edges


def _color_edges(edges, half):
    """Alternately labels edges top (0) / bottom (1), one cycle at a time."""
    in_edges = [[] for _ in range(half)]
    out_edges = [[] for _ in range(half)]
    for e in edges:
        in_edges[e["in_switch"]].append(e)
        out_edges[e["out_switch"]].append(e)

    color = {}
    for i in range(half):
        if all(e["id"] in color for e in in_edges[i]):
            continue
        _color_one_cycle(i, in_edges, out_edges, color)
    return color


def _color_one_cycle(start_switch, in_edges, out_edges, color):
    """Walks one cycle of the bipartite graph, flipping color at each step."""
    start_edge = next(e for e in in_edges[start_switch] if e["id"] not in color)
    color[start_edge["id"]] = 0

    side = "out"
    switch = start_edge["out_switch"]
    prev_edge = start_edge

    while True:
        node_edges = out_edges[switch] if side == "out" else in_edges[switch]
        other = next(e for e in node_edges if e["id"] != prev_edge["id"])
        if other["id"] in color:
            break
        color[other["id"]] = 1 - color[prev_edge["id"]]
        if side == "out":
            switch, side = other["in_switch"], "in"
        else:
            switch, side = other["out_switch"], "out"
        prev_edge = other


if __name__ == "__main__":
    # manual check: a random permutation, settings printed
    perm = [3, 1, 0, 2]
    settings = route_benes_permutation(perm)
    print(settings)
