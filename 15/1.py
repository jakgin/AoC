with open("in") as f:
    p1, p2 = f.read().strip().split("\n\n")

grid = []
for row in p1.split("\n"):
    grid.append([col for col in row])
moves = p2.replace("\n", "")

WALL = "#"
BOX = "O"
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
    for move in moves:
        # print("Move:", move)
        row, col = (robot_loc[0] + dirs[move][0], robot_loc[1] + dirs[move][1])
        val = grid[row][col]
        if val == EMPTY:
            grid[robot_loc[0]][robot_loc[1]] = EMPTY
            grid[row][col] = ROBOT
            robot_loc = (row, col)
        elif val == BOX:
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
        # show_grid(grid)


def calculate_gps_sum(grid):
    res = 0
    for row in range(1, H):
        for col in range(1, W):
            if grid[row][col] == BOX:
                res += 100 * row + col
    return res


make_moves(grid, moves)
show_grid(grid)
ans = calculate_gps_sum(grid)
print(ans)
