# Search Agent — Drone Delivery Route Planner
A Python implementation comparing Uniform Cost Search (UCS) and A* Search
to solve a delivery-drone routing problem under battery and capacity constraints.
## Problem
A drone starts at HQ with a full battery. It must:
1. Pick up orders at the restaurant (`R1`)
2. Deliver each order to its destination customer (`C1`, `C2`)
3. Recharge at HQ or the charging hub (`CH1`) when battery is low
4. Return to HQ once all orders are delivered

The environment is modeled as a weighted graph of locations, where each move
consumes battery and adds to the travel cost. The goal is to find the 
lowest-cost path that delivers all orders and returns to HQ.
## Project Structure
- `environment.py` — defines the map (graph), battery capacity, order capacity, and starting state
- `ucs.py` — Uniform Cost Search implementation
- `astar.py` — A* Search implementation with a location-based heuristic
- `main.py` — runs both algorithms and prints their resulting paths and total costs
## Usage

```bash
python main.py
```
This prints the path and total cost found by UCS, followed by the path and
total cost found by A*, so you can compare their efficiency.
## Notes
- Both algorithms operate on the same state space: `(location, carried_orders, delivered_orders, battery)`
- A* uses a heuristic combining estimated distance-to-goal and remaining undelivered orders to guide the search more efficiently than UCS
