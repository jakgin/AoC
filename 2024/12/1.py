with open("in") as f:
    grid = f.read().strip().split("\n")

h = len(grid)
w = len(grid[0])

ans = 0
seen = set()


def in_bounds(block):
    row, col = block
    return (0 <= row < h and 0 <= col < w)


def get_parameter(block):
    count = 0
    row, col = block
    directions = ((-1, 0), (0, 1), (1, 0), (0, -1))
    for d in directions:
        n_row = row + d[0]
        n_col = col + d[1]
        if in_bounds((n_row, n_col)):
            if not grid[n_row][n_col] == grid[row][col]:
                count += 1
        else:
            count += 1
    return count


def get_region(block, seen):
    val = grid[block[0]][block[1]]
    region = []
    q = set([block])
    while len(q) > 0:
        block = q.pop()
        region.append(block)
        seen.add(block)

        directions = ((-1, 0), (0, 1), (1, 0), (0, -1))
        for d in directions:
            n_row = block[0] + d[0]
            n_col = block[1] + d[1]
            if in_bounds((n_row, n_col)):
                if (n_row, n_col) not in seen and grid[n_row][n_col] == val:
                    q.add((n_row, n_col))

    return region


for row in range(h):
    for col in range(w):
        if (row, col) in seen:
            continue
        parameter = 0
        region = get_region((row, col), seen)
        for block in region:
            parameter += get_parameter(block)
        ans += parameter * len(region)

print(ans)