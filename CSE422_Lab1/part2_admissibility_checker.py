from collections import deque

def read_input(file_path):
    with open(file_path, 'r') as f:
        n, m = map(int, f.readline().split())
        a, b = map(int, f.readline().split())
        heuristics = {}
        for _ in range(n):
            x, y = map(int, f.readline().split())
            heuristics[x] = y
        edges = {i: [] for i in range(1, n+1)}
        for _ in range(m):
            u, v = map(int, f.readline().split())
            edges[u].append(v)
            edges[v].append(u)
    return n, m, a, b, heuristics, edges

def bfs_shortest_paths(goal, n, edges):
    dist = {i: float('inf') for i in range(1, n+1)}
    dist[goal] = 0
    queue = deque([goal])
    while queue:
        u = queue.popleft()
        for v in edges[u]:
            if dist[v] == float('inf'):
                dist[v] = dist[u] + 1
                queue.append(v)
    return dist

def check_admissibility(n, goal, heuristics, edges):
    dist = bfs_shortest_paths(goal, n, edges)
    inadmissible = []
    for node in heuristics:
        if heuristics[node] > dist[node]:
            inadmissible.append(node)
    return inadmissible

def write_output(file_path, inadmissible):
    with open(file_path, 'w') as f:
        if not inadmissible:
            f.write("1\n")
        else:
            f.write("0\n")
            f.write(" ".join(map(str, sorted(inadmissible))) + "\n")

if __name__ == "__main__":
    n, m, a, b, heuristics, edges = read_input("input2.txt")
    inadmissible = check_admissibility(n, b, heuristics, edges)
    write_output("output2.txt", inadmissible)