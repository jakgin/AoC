with open("in") as f:
    lines = f.read().strip().split("\n")

grid = []
for line in lines:
    row = [int(ch) for ch in line]
    grid.append(row)
h = len(grid)
w = len(grid[0])


def score(grid: list[list[int]], row: int, col: int):
    # DFS
    def get_neighbors(row, col):
        neighbors = []
        directions = ((0, -1), (-1, 0), (0, 1), (1, 0))
        for dr, dc in directions:
            n_row = row + dr
            n_col = col + dc
            if 0 <= n_row < h and 0 <= n_col < w and grid[row][col] + 1 == grid[n_row][n_col]:
                neighbors.append(((n_row, n_col), grid[n_row][n_col]))
        return neighbors
    
    seen_finish = set()
    stack = [((row, col), grid[row][col])]
    while len(stack) > 0:
        node = stack.pop()
        (row, col), val = node
        if val == 9:
            seen_finish.add((node))
        else:
            neighbors = get_neighbors(row, col)
            stack += neighbors
    return len(seen_finish)


scores = 0

for row in range(h):
    for col in range(w):
        if grid[row][col] == 0:
            scores += score(grid, row, col)     

print(scores)