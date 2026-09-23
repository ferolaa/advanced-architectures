"""
Traces every input's journey through the Looping Algorithm's
recursive splitting, for animating a whole permutation at once.

At each recursion level, every remaining pair of inputs splits into
"top" or "bottom". This function just records that sequence of
choices for every original input, all the way down to the base
case. No separate graph needs to be built or reconciled — this
walks the exact same recursion as route_benes_permutation itself.
"""

from routing.benes_routing import route_benes_permutation


def trace_all_inputs(perm):
    """
    Returns {input_index: [ "top"/"bottom", ... ]}, one list per
    original input, in the order the Looping Algorithm makes each
    top/bottom choice going deeper into the recursion.
    """
    n = len(perm)
    settings = route_benes_permutation(perm)
    traces = {x: [] for x in range(n)}

    def recurse(level_settings, level_n, positions):
        # positions[local_i] = original input index currently sitting
        # at local position local_i for this recursive call
        if level_n == 2:
            return
        half = level_n // 2
        first_stage = level_settings["first_stage"]
        top_positions = [None] * half
        bottom_positions = [None] * half
        for i in range(half):
            orig0 = positions[2 * i]
            orig1 = positions[2 * i + 1]
            if first_stage[i] == "straight":
                top_positions[i], bottom_positions[i] = orig0, orig1
                traces[orig0].append("top")
                traces[orig1].append("bottom")
            else:
                top_positions[i], bottom_positions[i] = orig1, orig0
                traces[orig1].append("top")
                traces[orig0].append("bottom")
        recurse(level_settings["top"], half, top_positions)
        recurse(level_settings["bottom"], half, bottom_positions)

    recurse(settings, n, list(range(n)))
    return traces


if __name__ == "__main__":
    perm = [3, 1, 0, 2]
    traces = trace_all_inputs(perm)
    for x, choices in traces.items():
        print(f"input {x} -> output {perm[x]}: {choices}")
