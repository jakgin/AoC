with open("input.txt") as f:
    lines = f.read().strip().split("\n")
    board = [list(line) for line in lines]

WIDTH = len(board[0])
HEIGHT = len(board)
OBSTRUCTION = "#"
BLANK = "."
DIRECTIONS = {"<": (-1, 0),
              "^": (0, -1),
              ">": (1, 0),
              "v": (0, 1)}

for y in range(HEIGHT):
    for x in range(WIDTH):
        if board[y][x] in DIRECTIONS:
            guard_position = (x, y, board[y][x])

def simulate(board, pos):
    # Returns True if there is a loop
    visited = set()
    potential_positions = set()
    while True:
        x, y, direction = pos
        new_x = DIRECTIONS[direction][0] + x
        new_y = DIRECTIONS[direction][1] + y
        if not (0 <= new_x < WIDTH) or not (0 <= new_y < HEIGHT):
            break
        next_direction = direction

        if board[new_y][new_x] == OBSTRUCTION:
            directions = tuple(DIRECTIONS.keys())
            cur_index = directions.index(direction)
            next_direction = directions[(cur_index + 1) % len(directions)]
            new_x = DIRECTIONS[next_direction][0] + x
            new_y = DIRECTIONS[next_direction][1] + y
            if board[new_y][new_x] == OBSTRUCTION:
                directions = tuple(DIRECTIONS.keys())
                cur_index = directions.index(next_direction)
                next_direction = directions[(cur_index + 1) % len(directions)]
                new_x = DIRECTIONS[next_direction][0] + x
                new_y = DIRECTIONS[next_direction][1] + y

        pos = (new_x, new_y, next_direction)
        if pos in visited:
            return potential_positions, True
        visited.add(pos)
        if ((pos[0], pos[1]) != (guard_position[0], guard_position[1])):
            potential_positions.add((pos[0], pos[1]))
    return potential_positions, False

ans = 0

potential_positions, _ = simulate(board, guard_position)
for x, y in potential_positions:
    board[y][x] = OBSTRUCTION
    _, loop = simulate(board, guard_position)
    if loop:
        ans += 1
    board[y][x] = BLANK

print(ans)


# Idea 1 - brute force - check every place guardian goes for a potential new obstruction -> check if there goes into a loop then
# Idea 2 - Idea 1 optimization - check if putting obstruction in a place will create the "rectangle", if not don't bother simulating this case

# not 1845