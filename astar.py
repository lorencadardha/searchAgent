import heapq
from environment import graph, MAX_BATTERY, MAX_CAPACITY, ORDERS

heuristic_values = {'HQ': 6, 'R1': 4, 'C1': 3, 'C2': 2, 'CH1': 2}

def heuristic(state):
    loc, carried, delivered, battery = state
    remaining = len(ORDERS) - len(delivered)
    # use .get to avoid KeyError for unexpected locations
    return heuristic_values.get(loc, 0) + remaining * 2

def _state_id(state):
    loc, carried, delivered, battery = state
    return (loc, tuple(sorted(carried)), tuple(sorted(delivered)), battery)

def a_star_search(start_state):
    # Heap entries: (f, g, state, path)
    queue = [(heuristic(start_state), 0, start_state, [])]
    # best g found so far for a canonical state id
    g_scores = {_state_id(start_state): 0}

    while queue:
        f, g, state, path = heapq.heappop(queue)
        loc, carried, delivered, battery = state

        # If we have already found a better g for this state, skip
        sid = _state_id(state)
        if g > g_scores.get(sid, float('inf')):
            continue

        # Goal: all orders delivered and back at HQ
        if set(delivered) == set(ORDERS) and loc == 'HQ':
            return g, path + [state]

        # Move to neighbors (consumes battery and costs step)
        for n, step in graph.get(loc, {}).items():
            if battery >= step:
                new_state = (n, list(carried), list(delivered), battery - step)
                new_g = g + step
                new_sid = _state_id(new_state)
                if new_g < g_scores.get(new_sid, float('inf')):
                    g_scores[new_sid] = new_g
                    heapq.heappush(queue, (new_g + heuristic(new_state), new_g, new_state, path + [state]))

        # Pickup orders at R1 (cost 0)
        if loc == 'R1':
            for o in ORDERS:
                if o not in carried and o not in delivered and len(carried) < MAX_CAPACITY:
                    new_carried = list(carried) + [o]
                    new_state = (loc, new_carried, list(delivered), battery)
                    new_g = g
                    new_sid = _state_id(new_state)
                    if new_g < g_scores.get(new_sid, float('inf')):
                        g_scores[new_sid] = new_g
                        heapq.heappush(queue, (new_g + heuristic(new_state), new_g, new_state, path + [state]))

        # Deliver orders at their destinations (cost 0)
        # map location -> order id to deliver
        deliveries = {'C1': 'O1', 'C2': 'O2'}
        if loc in deliveries:
            o = deliveries[loc]
            if o in carried:
                new_carried = list(carried)
                new_carried.remove(o)
                new_delivered = list(delivered) + [o]
                new_state = (loc, new_carried, new_delivered, battery)
                new_g = g
                new_sid = _state_id(new_state)
                if new_g < g_scores.get(new_sid, float('inf')):
                    g_scores[new_sid] = new_g
                    heapq.heappush(queue, (new_g + heuristic(new_state), new_g, new_state, path + [state]))

        # Recharge at HQ or CH1 (cost 1, restore battery)
        if loc in ['HQ', 'CH1'] and battery < MAX_BATTERY:
            new_state = (loc, list(carried), list(delivered), MAX_BATTERY)
            new_g = g + 1
            new_sid = _state_id(new_state)
            if new_g < g_scores.get(new_sid, float('inf')):
                g_scores[new_sid] = new_g
                heapq.heappush(queue, (new_g + heuristic(new_state), new_g, new_state, path + [state]))

    return float('inf'), []