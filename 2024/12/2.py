from collections import defaultdict

with open("in") as f:
    grid = f.read().strip().split("\n")

h = len(grid)
w = len(grid[0])

ans = 0
seen = set()


def in_bounds(block):
    row, col = block
    return (0 <= row < h and 0 <= col < w)


def get_sides(region: list[tuple[int]]) -> int:
    count = 0
    
    # Get the vertical and horizontal parameters with their coordinates
    vertical = []
    horizontal = []
    for block in region:
        vertical_d = ((-1, 0), (1, 0))
        horizontal_d = ((0, 1), (0, -1))
        for d in vertical_d:
            n_row = block[0] + d[0]
            n_col = block[1] + d[1]
            if in_bounds((n_row, n_col)):
                if grid[n_row][n_col] != grid[block[0]][block[1]]:
                    if n_row > block[0]:
                        horizontal.append((block[0] + 1, n_col, "down"))
                    else:
                        horizontal.append((block[0], n_col, "up"))
            else:
                if n_row > block[0]:
                    horizontal.append((block[0] + 1, n_col, "down"))
                else:
                    horizontal.append((block[0], n_col, "up"))
        for d in horizontal_d:
            n_row = block[0] + d[0]
            n_col = block[1] + d[1]
            if in_bounds((n_row, n_col)):
                if grid[n_row][n_col] != grid[block[0]][block[1]]:
                    if n_col > block[1]:
                        vertical.append((n_row, block[1] + 1, "right"))
                    else:
                        vertical.append((n_row, block[1], "left"))
            else:
                if n_col > block[1]:
                    vertical.append((n_row, block[1] + 1, "right"))
                else:
                    vertical.append((n_row, block[1], "left"))
    
    # Sort the parameters with the correct axes and check for holes
    grouped_vertical = defaultdict(list)
    for block in vertical:
        row, col, side = block
        grouped_vertical[(col, side)].append(row)
    grouped_horizontal = defaultdict(list)
    for block in horizontal:
        row, col, side = block
        grouped_horizontal[(row, side)].append(col)

    for blocks in grouped_vertical.values():
        blocks = sorted(blocks)
        holes = 0
        for i in range(len(blocks) - 1):
            if blocks[i] < blocks[i + 1] - 1:
                holes += 1
        count += holes + 1
    for blocks in grouped_horizontal.values():
        blocks = sorted(blocks)
        holes = 0
        for i in range(len(blocks) - 1):
            if blocks[i] < blocks[i + 1] - 1:
                holes += 1
        count += holes + 1

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
        sides = 0
        region = get_region((row, col), seen)
        area = len(region)
        sides = get_sides(region)
        ans += area * sides

print(ans)