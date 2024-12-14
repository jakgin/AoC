import re

with open("in") as f:
    lines = f.read().strip().split("\n")

w = 101
h = 103


def move(x, y, vx, vy, seconds):
    new_x = (x + seconds * vx) % w
    new_y = (y + seconds * vy) % h
    return new_x, new_y


def which_quarter(x, y):
    if 0 <= x < w // 2 and 0 <= y < h // 2:
        return 0
    if 0 <= x < w // 2 and h // 2 < y < h:
        return 1
    if w // 2 < x < w and h // 2 < y < h:
        return 2
    if w // 2 < x < w and 0 <= y < h // 2:
        return 3
    return 4


grid = []
for row in range(h):
    grid.append([0 for _ in range(w)])

quarters = [0, 0, 0, 0, 0]

for line in lines:
    x, y, vx, vy = [int(n) for n in re.findall(r"-*\d+", line)]
    new_x, new_y = move(x, y, vx, vy, 100)
    grid[new_y][new_x] += 1
    quarters[which_quarter(new_x, new_y)] += 1

for row in grid:
    print(row)

print(quarters)
print(quarters[0] * quarters[1] * quarters[2] * quarters[3])

