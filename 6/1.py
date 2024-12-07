with open("input.txt") as f:
    board = f.read().strip().split("\n")

WIDTH = len(board[0])
HEIGHT = len(board)
OBSTRUCTION = "#"
DIRECTIONS = {"<": (-1, 0),
              "^": (0, -1),
              ">": (1, 0),
              "v": (0, 1)}

visited_positions = set()

for y in range(HEIGHT):
    for x in range(WIDTH):
        if board[y][x] in DIRECTIONS:
            guard_position = (x, y, board[y][x])
            visited_positions.add((x, y))

ans = 1

while True:
    x, y, direction = guard_position
    new_x = DIRECTIONS[direction][0] + x
    new_y = DIRECTIONS[direction][1] + y
    if not (0 <= new_x < WIDTH) or not (0 <= new_y < HEIGHT):
        break

    next_x = DIRECTIONS[direction][0] + new_x
    next_y = DIRECTIONS[direction][1] + new_y
    if not (0 <= next_x < WIDTH) or not (0 <= next_y < HEIGHT):
        ans += 1
        break

    next_direction = direction
    if board[next_y][next_x] == OBSTRUCTION:
        directions = tuple(DIRECTIONS.keys())
        cur_index = directions.index(direction)
        next_direction = directions[(cur_index + 1) % len(directions)]

    guard_position = (new_x, new_y, next_direction)
    if (new_x, new_y) not in visited_positions:
        visited_positions.add((new_x, new_y))
        ans += 1

print(ans)