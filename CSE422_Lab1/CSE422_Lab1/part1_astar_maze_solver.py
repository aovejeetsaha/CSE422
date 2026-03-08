import heapq

def read_input(file_path):
    with open(file_path, 'r') as f:
        n, m = map(int, f.readline().split())
        a, b = map(int, f.readline().split())
        c, d = map(int, f.readline().split())
        maze = [list(f.readline().strip()) for _ in range(n)]
    return n, m, (a, b), (c, d), maze

def manhattan(p1, p2):
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])

def astar(n, m, start, goal, maze):
    directions = [(0, 1, 'R'), (1, 0, 'D'), (0, -1, 'L'), (-1, 0, 'U')]
    visited = set()
    heap = [(manhattan(start, goal), 0, start[0], start[1], '')]

    while heap:
        est_total, cost, x, y, path = heapq.heappop(heap)
        if (x, y) == goal:
            return cost, path
        if (x, y) in visited:
            continue
        visited.add((x, y))
        for dx, dy, move in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m and maze[nx][ny] == '0' and (nx, ny) not in visited:
                new_cost = cost + 1
                est = new_cost + manhattan((nx, ny), goal)
                heapq.heappush(heap, (est, new_cost, nx, ny, path + move))
    return -1, ''

def write_output(file_path, cost, path):
    with open(file_path, 'w') as f:
        f.write(f"{cost}\n")
        if cost != -1:
            f.write(f"{path}\n")

if __name__ == "__main__":
    n, m, start, goal, maze = read_input("input1.txt")
    cost, path = astar(n, m, start, goal, maze)
    write_output("output1.txt", cost, path)