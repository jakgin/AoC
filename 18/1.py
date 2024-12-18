from collections import deque


with open("in") as f:
    lines = f.read().strip().split("\n")

w = 71
h = 71


obstacles = set()
for line in lines[:1024]:
    x, y = line.split(",")
    obstacles.add((int(x), int(y)))

grid = []
for i in range(h):
    row = []
    for j in range(w):
        if (j, i) not in obstacles:
            row.append(".")
        else:
            row.append("#")
    grid.append(row)

for row in grid:
    for cell in row:
        print(cell, end="")
    print()

def shortest_path():
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


cost = shortest_path()
print(cost)