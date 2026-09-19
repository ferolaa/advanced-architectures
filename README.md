# Advanced Architectures Project

A small Python project about interconnection networks: networks
used to connect many processors together in a parallel computer.

## What it does

Three network types are built and routed:

- **Baseline network** — connects N inputs to N outputs through
  small 2x2 switches arranged in stages. Routing is done by
  self-routing: the destination address's bits decide the path.
- **Benes network** — two Baseline networks mirrored back to back.
  Any full input-output permutation can be routed with no clashes,
  using the Looping Algorithm.
- **Clos network** — a three-stage network (input, middle, output).
  Any input can reach any output through some middle switch.

For each network, the project can:
1. Build it as a graph.
2. Find a path (or a full routing) through it.
3. Draw a picture of it.

## Project files

- `networks/` — builds each network (`baseline.py`, `benes.py`, `clos.py`)
- `routing/` — finds paths through each network
- `tests/` — checks the routing against the built networks
- `pictures/` — saved drawings of each network
- `run_demo.py` — sends some traffic through all three networks
- `draw_networks.py` — draws and saves the three pictures
- `REPORT.md` — short write-up of the theory and results

## How to run it

Install the two libraries needed:
```
pip install networkx matplotlib
```

Build and print a network:
```
python3 networks/baseline.py
python3 -m networks.benes
python3 -m networks.clos
```

Run the routing checks:
```
python3 -m tests.check_baseline_routing
python3 -m tests.check_benes_routing
python3 -m tests.check_clos_routing
```

Run the traffic demo:
```
python3 run_demo.py
```

Draw the pictures:
```
python3 draw_networks.py
```
