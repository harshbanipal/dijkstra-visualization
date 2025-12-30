from math import inf
from priorityQue import MinPriorityQueue

def dijkstra(G, s):

    """
    dijkstra implementation from my algorithms class homework
    Graph format: G[u][v] = weight l(u, v) the weights might be integers or floats
    Returns:    d: a dict mapping node -> shortest distance from s, 
                parents: dict mapping node -> parent in shortest-path tree (s has parent None)
    """

    for u, neighbors in G.items():
        for v, weight in neighbors.items():
            if weight < 0:
                raise ValueError("Dijkstra requires non-negative edge weights; found negative weight")


    # Collect all vertices (include isolated / sink nodes that might only appear as neighbors)
    vertices = set(G.keys())

    # pi: current best-known distances (keys)
    pi = {}

    # d: finalized shortest distances
    d = {}

    # parents in shortest paths tree
    parents = {s: None}

    # number of edges to reach source 
    numEdges = {}


    # your implementation from part 1
    Q = MinPriorityQueue()


    # Initialize source
    pi[s] = 0.0
    numEdges[s] = 0
    Q.insert(s, (0.0, 0))


    # Initialize all other vertices to infinity
    for v in vertices:
        if v == s:
            continue
        pi[v] = inf
        numEdges[v] = inf
        parents.setdefault(v, None)
        Q.insert(v, (inf, inf))


    # Main loop
    while Q.heap:
        u, (path_length_u, edge_length_u) = Q.extract_min()  # returns (element, priority)
        d[u] = path_length_u
        if path_length_u == inf:
            continue

        # For each neighbor v of u
        for v, weight_uv in G[u].items():
            # Update the best path length to v using edge (u, v) if it improves pi[v]
            if (pi[v], numEdges[v]) > (d[u] + weight_uv, edge_length_u + 1):
                new_priority = (d[u] + weight_uv, edge_length_u +1)
                Q.decrease_key(v, new_priority)
                pi[v] = new_priority[0]
                parents[v] = u
                numEdges[v] = edge_length_u + 1

    return d, parents


