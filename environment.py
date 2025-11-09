# Graph = map of locations and travel costs
graph = {

    'HQ': {'R1': 2, 'CH1': 4},          # HQ -> Restaurant R1 or Charging Hub CH1
    'R1': {'C1': 3, 'CH1': 2},          # Restaurant -> Customer or Charging
    'C1': {'C2': 4, 'CH1': 3},          # Customer 1 -> Customer 2 or Charging
    'C2': {'CH1': 3, 'HQ': 5},          # Customer 2 -> Charging or HQ
    'CH1': {'HQ': 4, 'C2': 3, 'C1': 3}  # Charging Hub connects to HQ or C2 or C1

}

MAX_BATTERY = 6               #maximum battery capacity of the drone
MAX_CAPACITY = 2              #maximum number of orders the drone can carry at once
ORDERS = ['O1', 'O2']         #list of orders that need to be delivered.
start_state = ('HQ', [], [], MAX_BATTERY) #right now the drone is at HQ, carrying no orders, has delivered no orders, and has full battery
