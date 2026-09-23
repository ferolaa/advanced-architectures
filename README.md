# Advanced Architectures Project

A Python project about interconnection networks: networks that
connect many processors together in a parallel computer.

## What it does

Four network types, built and routed:

- **Baseline** — small 2x2 switches in stages. Routes by reading
  bits of the destination address.
- **Benes** — two Baseline networks mirrored together. Can route
  any full permutation with no clashes, using the Looping Algorithm.
- **Clos** — input, middle, and output switches. Many paths exist
  between any input and output.
- **XGFT fat-tree** — a tree with more parallel links near the top.

For each network: build it, find paths through it, draw it.

## Easiest way to see it

Open `network_demo.html` in a browser. Nothing to install or run —
pictures, animations, and every check's real output are already
built into the page.

## Project files

- `networks/` — builds each network
- `routing/` — finds paths through each network
- `tests/` — checks routing against the built networks
- `pictures/` — saved drawings
- `run_demo.py` — traffic demo for all four networks
- `draw_networks.py` — saves the network pictures
- `scaling_analysis.py` — plots how network size grows
- `blocking_analysis.py` — plots Clos blocking rate vs middle switches
- `network_demo.html` — animated, interactive version of everything above
- `run_all.py` — runs every step below in one command
- `export_demo_data.py`, `export_blocking_demo.py` — generate the data built into `network_demo.html`
- `report/` — the written report (LaTeX)

## How to run it

Install:
```
pip install networkx matplotlib
```

Run everything in one go:
```
python3 run_all.py
```

Or run each step by hand:
```
python3 networks/baseline.py
python3 -m networks.benes
python3 -m networks.clos
python3 -m networks.xgft

python3 -m tests.check_baseline_routing
python3 -m tests.check_benes_routing
python3 -m tests.check_clos_routing
python3 -m tests.check_xgft_routing
python3 -m tests.check_clos_blocking

python3 run_demo.py
python3 draw_networks.py
python3 scaling_analysis.py
python3 blocking_analysis.py
```

`export_demo_data.py` and `export_blocking_demo.py` only need
running again if you change a network's example settings and want
`network_demo.html` updated to match.
