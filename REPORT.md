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

For the Clos network, the middle switch count m was also varied
while keeping the number of inputs fixed (`pictures/scaling_clos_by_m.png`).
More middle switches means more redundant paths (helpful for
avoiding blocking), but the cost is not free: the number of wires
grows much faster than the number of switches, since every middle
switch added connects to all r input and all r output switches.
This is the cost/redundancy trade-off behind Clos's non-blocking
condition (m >= 2n - 1).

## Comparing all four topologies

Switch counts for all four networks were plotted together
(`pictures/scaling_all_topologies.png`), all set up to be
non-blocking so the comparison is fair: Baseline, Benes and XGFT
(with redundancy w=2) are non-blocking (or close to it) by
construction, and Clos uses m = 2n - 1, the proven non-blocking
minimum.

Clos comes out with the fewest switches in this comparison. This
is because its r and n were both set to roughly sqrt(N), so its
switch count grows with sqrt(N) rather than N or N*log(N) like the
other three. This is a property of the chosen r/n split, not a
general rule for every Clos network — but it does show why Clos
networks are popular in real data centers, where the number of
switches (and their cost) matters a lot.

## Blocking analysis

Clos's theorem says a network with m >= 2n - 1 middle switches can
always route any traffic with no blocking, no matter how the calls
are arranged. This was tested directly (`blocking_analysis.py`,
plot in `pictures/blocking_rate.png`): many random traffic patterns
were generated for a range of m values, and the fraction of blocked
calls was measured.

Below the threshold, blocking happens often, and gets rarer as m
grows. For r=8, n=5, the threshold is m = 2*5 - 1 = 9. In the
random trials, the blocking rate actually reached zero a bit
earlier (around m=6-7), not exactly at m=9. This is not a mistake:
the m >= 2n - 1 guarantee holds for the *worst possible* traffic
pattern, which is unlikely to come up by chance in random tests.
Random traffic tends to avoid the worst case, so it can look
non-blocking earlier — but only m >= 2n - 1 guarantees it always,
for every possible pattern.

## What was left out

To keep the project simple, blocking analysis (how likely a
network is to run out of free paths under load) was not
implemented. This could be a natural extension.
