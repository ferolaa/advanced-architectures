# Advanced Architectures Project

This project builds a few types of computer networks (used to connect many
processors together) and shows how data moves through them.

## What it does

We build these networks:
- **Baseline / Butterfly network** — a simple network that uses the bits of
  the destination address to pick the path.
- **Beneš network** — a network that can connect any input to any output
  with no clashes, if you route it the right way.
- **Clos network** — a network built in stages, often used in real
  data centers.

For each network, we can:
1. Build it (as a graph of switches and connections).
2. Send data through it and find the path from input to output.
3. Draw a picture of it.

## Why

This is the project for the Advanced Architectures course
(computer architecture / parallel computing). It shows the
interconnection network part of the course with real code.

## Project files

- `networks/` — code that builds each network
- `routing/` — code that finds the path through each network
- `tests/` — small checks comparing our code to the numbers from class
- `pictures/` — saved drawings of each network

## How to run it

(coming soon, as each part is finished)
