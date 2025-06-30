with open("in") as f:
    lines = f.read().strip().split("\n")
    grid = []
    for row in lines:
        n_row = []
        for ch in row:
            n_row.append(ch)
        grid.append(n_row)


def show_grid(grid):
    for row in grid:
        for ch in row:
            print(ch, end="")
        print()


def get_nbs(grid, place):
    row, col = place
    dirs = {
        "S": [(-1, 0), (0, 1), (1, 0), (0, -1)],
        "|": [(-1, 0), (1, 0)],
        "-": [(0, -1), (0, 1)],
        "L": [(-1, 0), (0, 1)],
        "J": [(-1, 0), (0, -1)],
        "7": [(1, 0), (0, -1)],
        "F": [(1, 0), (0, 1)],
        ".": [],
    }
    symbol = grid[row][col]
    nbs = []
    for d in dirs[symbol]:
        n_row, n_col = row + d[0], col + d[1]
        if 0 <= n_row < len(grid) and 0 <= n_col < len(grid[0]):
            if symbol == "S":
                back_nbs = get_nbs(grid, (n_row, n_col))
                if place not in back_nbs:
                    continue
            nbs.append((n_row, n_col))
    return nbs


# Find start
for row in range(len(grid)):
    for col in range(len(grid[0])):
        if grid[row][col] == "S":
            s = (row, col)

nbs = get_nbs(grid, s)
assert len(nbs) == 2
start, end = nbs

loop = []
seen = set([s, start])
stack = [start]
prevs = {}

while stack:
    item = stack.pop()
    if item == end:
        while item:
            loop.append(item)
            item = prevs.get(item)
        break
    for nb in get_nbs(grid, item):
        if nb not in seen: 
            stack.append(nb)
            seen.add(nb)
            prevs[nb] = item

print(len(loop) // 2 + 1)