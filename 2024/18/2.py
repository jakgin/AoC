from collections import deque


with open("in") as f:
    lines = f.read().strip().split("\n")
    tmp = []
    for line in lines:
        x, y = line.split(",")
        tmp.append((int(x), int(y)))
    lines = tmp

w = 71
h = 71


def shortest_path():
    # BFS
    def neighbors(coord):
        nbors = []
        x, y, cost = coord
        dirs = ((0, -1), (1, 0), (0, 1), (-1, 0))
        for dx, dy in dirs:
            nx = x + dx
            ny = y + dy
            if not (0 <= nx < w and 0 <= ny < h):
                continue
            if (nx, ny) not in seen and (nx, ny) not in obstacles:
                nbors.append((nx, ny, cost + 1))
                seen.add((nx, ny))
        return nbors

    start = (0, 0, 0)  # x, y, cost
    q = deque([start])
    seen = set((0, 0))
    while len(q) > 0:
        x, y, cost = q.popleft()
        if x == w - 1 and y == h - 1:
            return cost
        q += neighbors((x, y, cost))
    return -1


# Binary Search

low, high = 1024, len(lines) - 1

while low <= high:
    mid = low + (high - low) // 2
    obstacles = set(lines[:mid])
    cost = shortest_path()
    if cost != -1:
        obstacles.add(lines[mid])
        cost = shortest_path()
        if cost == -1:
            x, y = lines[mid]
            print(f"{x},{y}")
            break
        else:
            low = mid
    else:
        high = mid - 1
