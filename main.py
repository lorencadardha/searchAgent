from environment import start_state
from ucs import uniform_cost_search
from astar import a_star_search

def main():
    ucs_cost, ucs_path = uniform_cost_search(start_state)
    

    print("========== UCS PATH ==========")
    for step in ucs_path:
        print(step)
    print("Total UCS Cost:", ucs_cost)

    

if __name__ == "__main__":
    main()
