"""CMPE 365 Lab 2 / Assignment 1

2019-09-21 (3 Weeks: 10-12)

Troy Giorshev
20012707
15tag2

I certify that this submission contains my own work, except as noted.

==Assumptions==

I assume that flights departing at time 0 are allowed to be taken.

==Other Notes==

Finally got around to using YAPF to format

W is 2D, ROW then COL (ROW-major order)
Where ROW is "from" and COL is "to"
Each element of W will be a list of Flight objects from ROW to COL
If there are no flights, then there will simply be an empty list
e.g. W[0][1][0] will be the first Flight from 0 to 1
"""

import sys

INFINITY = sys.maxsize

class Flight:
    """Class for holding flight data"""
    def __init__(self, departure: int, arrival: int) -> None:
        self.departure = departure
        self.arrival = arrival


def get(filename: str) -> (int, list):
    """Reads the list of flights"""
    with open(filename) as f:
        cities = int(f.readline())
        W = [[[] for _ in range(cities)] for _ in range(cities)]
        for line in f:
            from_city, to_city, departure, arrival = map(int, line.split())
            W[from_city][to_city].append(Flight(departure, arrival))
    return cities, W


def get_cost(F: list, time: int) -> int:
    """Get the arrival time of the first flight that we can make"""
    global INFINITY
    try:
        # Flights leaving at time 0 are ALLOWED
        def cond(f, t):
            return (f.departure > t) or (t == 0 and f.departure == 0)

        valid = list(f for f in F if cond(f, time))
        valid.sort(key=lambda f: f.arrival)

        return valid[0].arrival
    except:
        # We've missed the last flight!
        # Or, there are no flights
        return INFINITY


def dijkstra(size: int, W: list, start: int, end: int) -> (list, int):
    """Find shortest route between start and end.

    Uses a modified Dijstra's algorithm.

    Args:
        size:   Number of cities
        W:      Flight weight matrix as described in the script docstring
        start:  Starting city
        end:    Ending city
    Returns:
        List of cities in the optimal route, in order
        Cost of the route
    """
    global INFINITY

    # Node arrays
    costs = [INFINITY] * size
    reached = [False] * size
    estimates = [INFINITY] * size
    candidates = [False] * size

    prevs_estimate = [-1] * size
    # "Which city were you at when you set the cost estimate"

    costs[start] = 0
    reached[start] = True
    prevs_estimate[start] = start

    for x in range(size):
        cost = get_cost(W[start][x], costs[start])
        if cost != INFINITY:
            # Neighbor of Start
            estimates[x] = cost
            candidates[x] = True
            prevs_estimate[x] = start

    while costs[end] == INFINITY:  # End early
        # Find lowest cost candidate
        best_cost = INFINITY
        v = None
        for x in range(size):
            if candidates[x] and estimates[x] < best_cost:
                best_cost = estimates[x]
                v = x
        if v == None:
            break

        # Set things that we know are true
        costs[v] = estimates[v]
        estimates[v] = INFINITY
        reached[v] = True
        candidates[v] = False

        # Update estimates and candidates
        for y in range(size):
            cost = get_cost(W[v][y], costs[v])
            if cost != INFINITY and not reached[y]:
                candidates[y] = True
                if cost < estimates[y]:
                    estimates[y] = cost
                    prevs_estimate[y] = v

    # Make the trip stack
    stack = [end]
    curr = end
    while prevs_estimate[curr] != start:
        stack.append(prevs_estimate[curr])
        curr = prevs_estimate[curr]

    stack.append(start)
    return (stack, costs[end])


def good_print(stack: list, cost: int, start: int, end: int) -> None:
    """Output as specified in I/O specifications"""
    if cost == INFINITY:
        print("No route found!")
    print(f"Optimal route from {start} to {end}")
    print()
    while (len(stack) != 1):
        print(f"Fly from {stack.pop()} to {stack[-1]}")
    print()
    print(f"Arrive at {end} at time {cost}")


if __name__ == "__main__":
    #start = int(input("From: "))
    #end = int(input("To: "))
    student_number = input("Student Number: ")
    start = int(student_number[-2:])
    end = int(student_number[-4:-2])
    print()

    good_print(
        *dijkstra(*get("Lab2/2019_Lab_2_flights_real_data.txt"), start, end),
        start, end)

    # I'm sure there was a good way to format that chained function call...
    # Sorry
