import heapq
from environment import graph, MAX_BATTERY, MAX_CAPACITY, ORDERS

def uniform_cost_search(start_state):
    # Priority queue: (total_cost_so_far, current_state, path_taken)
    queue = [(0, start_state, [])]  
    visited = set()  # Keep track of visited states

    step_counter = 0  # Optional counter for limiting expansions

    while queue:
        cost, state, path = heapq.heappop(queue)
        location, carried, delivered, battery = state
        step_counter += 1

        # Goal test: all orders delivered and at HQ
        if set(delivered) == set(ORDERS) and location == 'HQ':
            return cost, path + [state]

        # Skip already visited states (location + carried + delivered + battery)
        state_id = (location, tuple(sorted(carried)), tuple(sorted(delivered)), battery)
        if state_id in visited:
            continue
        visited.add(state_id)

        # 1️⃣ Move to neighboring locations if battery allows
        for neighbor, step_cost in graph[location].items():
            if battery >= step_cost:
                new_state = (neighbor, carried[:], delivered[:], battery - step_cost)
                heapq.heappush(queue, (cost + step_cost, new_state, path + [state]))

        # 2️⃣ Pick up orders at R1 if capacity allows
        if location == 'R1':
            for order in ORDERS:
                if order not in carried and order not in delivered and len(carried) < MAX_CAPACITY:
                    new_carried = carried + [order]
                    new_state = (location, new_carried, delivered[:], battery)
                    heapq.heappush(queue, (cost, new_state, path + [state]))

        # 3️⃣ Deliver orders at their destinations
        if location == 'C1' and 'O1' in carried:
            new_carried = carried[:]; new_carried.remove('O1')
            new_delivered = delivered + ['O1']
            new_state = (location, new_carried, new_delivered, battery)
            heapq.heappush(queue, (cost, new_state, path + [state]))

        if location == 'C2' and 'O2' in carried:
            new_carried = carried[:]; new_carried.remove('O2')
            new_delivered = delivered + ['O2']
            new_state = (location, new_carried, new_delivered, battery)
            heapq.heappush(queue, (cost, new_state, path + [state]))

        # 4️⃣ Recharge battery at HQ or CH1
        if location in ['HQ', 'CH1'] and battery < MAX_BATTERY:
            new_state = (location, carried[:], delivered[:], MAX_BATTERY)
            heapq.heappush(queue, (cost + 1, new_state, path + [state]))

    # If no valid path found, return infinity
    return float('inf'), []