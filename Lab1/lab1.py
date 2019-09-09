import pprint
import sys
import os

INFINITY = sys.maxsize
pp = pprint.PrettyPrinter()

# Read data
def get(filename: str) -> (int, list):
    global pp

    with open(filename) as f:
        nodes = int(f.readline())
        W = []
        for x in range(nodes):
            tmp = f.readline().split()
            W.append([])
            for j in range(nodes):
                W[x].append(int(tmp[j]))
        #pp.pprint(W)
    #print(f"The graph has {nodes} nodes.")
    return nodes, W

def dijkstra(size: int, W: list) -> (int, int): # That's the wrong return type syntax
    global INFINITY

    # Node arrays
    costs = [INFINITY]*size
    reached = [False]*size
    estimates = [INFINITY]*size
    candidates = [False]*size

    costs[0] = 0
    reached[0] = True

    for x in range(size):
        if W[0][x] != 0:
            # Neighbor of A
            estimates[x] = W[0][x]
            candidates[x] = True

    #while INFINITY in costs:
    while costs[end] == INFINITY:
        # Find lowest cost candidate
        best_cost = INFINITY
        v = None
        for x in range(size):
            if candidates[x] and estimates[x] < best_cost:
                    best_cost = estimates[x]
                    v = x

        costs[v] = estimates[v]
        reached[v] = True
        candidates[v] = False

        for y in range(size):
            if W[v][y] > 0 and not reached[y]:
                if costs[v] + W[v][y] < estimates[y]:
                    estimates[y] = costs[v] + W[v][y]
                    candidates[y] = True

    worst = None
    tmp = 0
    for x in range(len(costs)):
        if costs[x] > tmp:
            worst = x
            tmp = costs[x]
    
    return (worst, costs[worst])

if __name__ == "__main__":
    print()
    files = list(filter(lambda s: s.startswith('Dijkstra_Data_'), os.listdir()))
    files = sorted(files, key = lambda s: int(s[:-4][14:]))
    for f in files:
        worst, cost = dijkstra(*get(f))
        print(f"{f[:-4][14:]}: The highest cost node is {worst}, with cost {cost}")
