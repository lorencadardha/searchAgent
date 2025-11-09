import heapq
from environment import graph, MAX_BATTERY, MAX_CAPACITY, ORDERS

heuristic_values = {'HQ': 6, 'R1': 4, 'C1': 3, 'C2': 2, 'CH1': 2}
def heuristic(state):
    loc, carried, delivered, battery = state
    remaining = len(ORDERS) - len(delivered)
    return heuristic_values[loc] + remaining * 2

def a_star_search(start_state):
    queue = [(heuristic(start_state), 0, start_state, [])]  # f, g, state, path
    visited = set()

    while queue:
        f, g, state, path = heapq.heappop(queue)
        loc, carried, delivered, battery = state

        if set(delivered) == set(ORDERS) and loc == 'HQ':
            return g, path + [state]

        state_id = (loc, tuple(sorted(carried)), tuple(sorted(delivered)), battery)
        if state_id in visited:
            continue
        visited.add(state_id)

        # Move to neighbors
        for n, step in graph[loc].items():
            if battery >= step:
                new_state = (n, carried[:], delivered[:], battery - step)
                heapq.heappush(queue, (g + step + heuristic(new_state), g + step, new_state, path + [state]))

        # Pickup orders
        if loc == 'R1':
            for o in ORDERS:
                if o not in carried and o not in delivered and len(carried) < MAX_CAPACITY:
                    new_state = (loc, carried + [o], delivered[:], battery)
                    heapq.heappush(queue, (g + heuristic(new_state), g, new_state, path + [state]))

        # Deliver orders
        if loc == 'C1' and 'O1' in carried:
            new_carried = carried[:]; new_carried.remove('O1')
            new_delivered = delivered + ['O1']
            new_state = (loc, new_carried, new_delivered, battery)
            heapq.heappush(queue, (g + heuristic(new_state), g, new_state, path + [state]))
        if loc == 'C2' and 'O2' in carried:
            new_carried = carried[:]; new_carried.remove('O2')
            new_delivered = delivered + ['O2']
            new_state = (loc, new_carried, new_delivered, battery)
            heapq.heappush(queue, (g + heuristic(new_state), g, new_state, path + [state]))

        # Recharge
        if loc in ['HQ', 'CH1'] and battery < MAX_BATTERY:
            new_state = (loc, carried[:], delivered[:], MAX_BATTERY)
            heapq.heappush(queue, (g + 1 + heuristic(new_state), g + 1, new_state, path + [state]))

    return float('inf'), []
