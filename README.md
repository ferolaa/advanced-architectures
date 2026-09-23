# Advanced Architectures Project

A small Python project about interconnection networks: networks
used to connect many processors together in a parallel computer.

## What it does

Four network types are built and routed:

- **Baseline network** — connects N inputs to N outputs through
  small 2x2 switches arranged in stages. Routing is done by
  self-routing: the destination address's bits decide the path.
- **Benes network** — two Baseline networks mirrored back to back.
  Any full input-output permutation can be routed with no clashes,
  using the Looping Algorithm.
- **Clos network** — a three-stage network (input, middle, output).
  Any input can reach any output through some middle switch.

- **XGFT fat-tree** — a tree-shaped network with h levels. Higher
  levels have more parallel switches ("fat"), giving more possible
  paths near the top.

For each network, the project can:
1. Build it as a graph.
2. Find a path (or a full routing) through it.
3. Draw a picture of it.

## Project files

- `networks/` — builds each network (`baseline.py`, `benes.py`, `clos.py`, `xgft.py`)
- `routing/` — finds paths through each network
- `tests/` — checks the routing against the built networks
- `pictures/` — saved drawings of each network
- `run_demo.py` — sends some traffic through all four networks
- `draw_networks.py` — draws and saves the four pictures
- `scaling_analysis.py` — measures and plots how network size grows
- `blocking_analysis.py` — measures and plots Clos blocking rate vs middle switch count
- `export_demo_data.py` — exports real network data (built with the actual code above) for the page below
- `export_blocking_demo.py` — exports the live Clos blocking data for the page below
- `network_demo.html` — an animated page: pick a network and a source/destination and watch the real routing code find the path, plus a live side-by-side Clos blocking demo

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
python3 -m networks.xgft
```

Run the routing checks:
```
python3 -m tests.check_baseline_routing
python3 -m tests.check_benes_routing
python3 -m tests.check_clos_routing
python3 -m tests.check_xgft_routing
python3 -m tests.check_clos_blocking
```

Run the traffic demo:
```
python3 run_demo.py
```

Draw the pictures:
```
python3 draw_networks.py
```

Measure and plot how network size grows:
```
python3 scaling_analysis.py
```

Measure and plot Clos blocking behavior:
```
python3 blocking_analysis.py
```

See an animated, interactive demo: just open `network_demo.html`
in a browser — no server, no setup needed (its data is already
built in). Run `python3 draw_networks.py`, `scaling_analysis.py`
and `blocking_analysis.py` first if the pictures section further
down the page looks empty.

`export_demo_data.py` and `export_blocking_demo.py` are the
scripts that produced `network_demo.html`'s built-in data in the
first place — only run them (and re-embed their output) if you
change a network's example settings and want the page updated.
