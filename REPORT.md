# Report — Interconnection Networks Project

## Goal

The project studies three kinds of interconnection networks used
in parallel computers, and shows how data is routed through each
one, in code.

## The three networks

### Baseline network

Made of small 2x2 switches arranged in stages. For N inputs,
log2(N) stages of N/2 switches each are needed. Every switch has
two possible outputs: "straight" or "cross".

Routing is self-routing: at stage k, the k-th bit of the
destination address decides straight or cross. No searching is
needed, the path is read directly from the address.

### Benes network

Built from two Baseline networks placed back to back, sharing a
middle stage. For N inputs, it has 2*log2(N) - 1 stages.

Unlike the Baseline network, the Benes network can route any full
permutation (every input reaching a different output) without any
two paths clashing. This needs the **Looping Algorithm**:

1. Inputs and outputs are matched into a graph.
2. This graph is split into cycles.
3. Each cycle is colored alternately "top" or "bottom", deciding
   which half of the network each connection uses.
4. The same problem is solved again, twice, but at half size —
   once for the top half, once for the bottom half.
5. This repeats until each half is just one switch.

### Clos network

A three-stage network: input switches, middle switches, output
switches. Every input switch connects to every middle switch, and
every middle switch connects to every output switch. So many
different paths exist between any input and any output, and one is
picked using a simple rule.

## Results

- All three networks were built for different sizes and checked
  against the known switch/wire counts from class.
- Baseline routing was checked for every input-output pair in
  networks of size 8 and 16: every path found was a real wire.
- Benes routing was checked with 60 random full permutations
  (sizes 4, 8, 16): every one was routed correctly, confirmed by
  simulating the switch settings and comparing to the original
  permutation.
- Clos routing was checked for every input-output pair in two
  different configurations: every path found was a real wire.
- Pictures of each network were drawn and match the expected shape
  from the theory (see `pictures/`).

## Scaling analysis

The switch and wire counts of each network were measured as the
number of inputs grows (`scaling_analysis.py`, plots in
`pictures/scaling_baseline_benes.png` and `pictures/scaling_clos.png`).

The Benes network needs close to double the switches of the
Baseline network for the same size, which matches the theory: a
Benes network has 2*log2(N) - 1 stages, almost twice the
log2(N) stages of a Baseline network. Both grow with N*log(N),
not N*N, which is what makes these networks efficient for large
numbers of processors.

## What was left out

To keep the project simple, blocking analysis (how likely a
network is to run out of free paths under load) was not
implemented. This could be a natural extension.
