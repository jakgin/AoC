from collections import deque
from tqdm import tqdm


with open("in") as f:
    lines = f.read().strip().split("\n")

grid = []

for y, line in enumerate(lines):
    row = []
    no_wall_row = []
    for x, cell in enumerate(line):
        if cell == "S":
            start = (y, x)
        elif cell == "E":
            end = (y, x)
        row.append(cell) 
    grid.append(row)

h = len(grid)
w = len(grid[0])

def show_grid():
    for row in grid:
        for cell in row:
            print(cell, end="")
        print()


class Node:
    def __init__(self, coords, steps, prev):
        self.coords = coords
        self.steps = steps
        self.prev = prev

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        if self.coords == other.coords and self.steps == other.steps:
            return True
        return False

    
def neighbors(grid, cell, seen):
    y, x = cell
    dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    nbors = []
    for dy, dx in dirs:
        ny = y + dy
        nx = x + dx
        if not (0 <= ny < h and 0 <= nx < w):
            continue
        if grid[ny][nx] != "#" and (ny, nx) not in seen:
            nbors.append((ny, nx))
    return nbors


def shortest_path(grid, cheat):
    seen = set(start)
    q = deque([Node(start, 0, None)])

    while len(q) > 0:
        node = q.popleft()
        if node.coords == end:
            return node
        if cheat:
            cheat_coords, cheat_next_coords = cheat
            if node.coords == cheat_coords:
                cy, cx = cheat_next_coords
                grid[cy][cx] = "."
                nbors = neighbors(grid, node.coords, seen)
                grid[cy][cx] = "#"
            else:
                nbors = neighbors(grid, node.coords, seen)
        else:
            nbors = neighbors(grid, node.coords, seen)
        for nbor in nbors:
            q.append(Node(nbor, node.steps + 1, node))
            seen.add(nbor)
    return None


node = shortest_path(grid, None)
steps_no_cheat = node.steps

# Get nodes where to cheat
cheats = []
for y in range(h):
    for x in range(w):
        if grid[y][x] in ["#", "E"]:
            continue
        dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        for dy, dx in dirs:
            if grid[y + dy][x + dx] == "#":
                cheats.append(((y, x), (y + dy, x + dx)))
print("len of cheats", len(cheats))

ans = 0
for cheat in tqdm(cheats):
    end_node = shortest_path(grid, cheat)
    diff = steps_no_cheat - end_node.steps
    if diff >= 100:
        ans += 1

print("ans", ans)
