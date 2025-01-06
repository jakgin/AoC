with open("in") as f:
    p1, p2 = f.read().strip().split("\n\n")

grid = []
for row in p1.split("\n"):
    n_row = []
    for cell in row:
        if cell == "#":
            n_row.append("#")
            n_row.append("#")
        elif cell == "O":
            n_row.append("[")
            n_row.append("]")
        elif cell == ".":
            n_row.append(".")
            n_row.append(".")
        elif cell == "@":
            n_row.append("@")
            n_row.append(".")
    grid.append(n_row)
moves = p2.replace("\n", "")

WALL = "#"
BOX_L = "["
BOX_R = "]"
ROBOT = "@"
EMPTY = "."
H = len(grid)
W = len(grid[0])


def show_grid(grid):
    for row in grid:
        for cell in row:
            print(cell, end="")
        print()


def make_moves(grid, moves):
    dirs = {"<": (0, -1), "^": (-1, 0), ">": (0, 1), "v": (1, 0)}
    for row in range(H):
        for col in range(W):
            if grid[row][col] == ROBOT:
                robot_loc = (row, col)
    for index, move in enumerate(moves):
        # print(f"Move {index}:", move)
        row, col = (robot_loc[0] + dirs[move][0], robot_loc[1] + dirs[move][1])
        val = grid[row][col]
        if val == EMPTY:
            grid[robot_loc[0]][robot_loc[1]] = EMPTY
            grid[row][col] = ROBOT
            robot_loc = (row, col)
        elif val in (BOX_L, BOX_R) and move in ["<", ">"]:
            while True:
                row, col = row + dirs[move][0], col + dirs[move][1]
                val = grid[row][col]
                if val == WALL:
                    break
                if val == EMPTY:
                    curr_row, curr_col = row, col
                    while True:
                        prev_row = curr_row - dirs[move][0]
                        prev_col = curr_col - dirs[move][1]
                        prev_val = grid[prev_row][prev_col]
                        grid[curr_row][curr_col] = prev_val
                        if prev_val == ROBOT:
                            robot_loc = (curr_row, curr_col)
                            grid[prev_row][prev_col] = EMPTY
                            break
                        curr_row = prev_row
                        curr_col = prev_col
                    break
        elif val in (BOX_L, BOX_R):
            def add_box(blocks, lvl, row, col, val):
                if len(blocks) <= lvl:
                    blocks.append([])
                if (row, col) in blocks[lvl]:
                    return
                blocks[lvl].append((row, col))
                if val == BOX_L:
                    blocks[lvl].append((row, col + 1))
                else:
                    blocks[lvl].append((row, col - 1))

            blocks = [[robot_loc]]
            add_box(blocks, 1, row, col, val)
            lvl = 2
            while True:
                row_blocks = blocks[-1]
                hit_wall = False
                empty_count = 0
                for block in row_blocks:
                    row, col = block[0] + dirs[move][0], block[1] + dirs[move][1]
                    val = grid[row][col]
                    if val == WALL:
                        hit_wall = True
                        break
                    elif val in (BOX_L, BOX_R):
                        add_box(blocks, lvl, row, col, val)
                    elif val == EMPTY:
                        empty_count += 1
                        if empty_count < len(row_blocks):
                            continue
                        for row_blocks in reversed(blocks):
                            for block in row_blocks:
                                n_block_row = block[0] + dirs[move][0]
                                n_block_col = block[1] + dirs[move][1]
                                grid[n_block_row][n_block_col] = grid[block[0]][block[1]]
                                grid[block[0]][block[1]] = EMPTY
                        robot_loc = (robot_loc[0] + dirs[move][0], robot_loc[1] + dirs[move][1])
                        hit_wall = True
                        break
                if hit_wall:
                    break
                lvl += 1
        # show_grid(grid)


def calculate_gps_sum(grid):
    res = 0
    for row in range(1, H):
        for col in range(1, W):
            if grid[row][col] == BOX_L:
                res += 100 * row + col
    return res


make_moves(grid, moves)
show_grid(grid)
ans = calculate_gps_sum(grid)
print(ans)
