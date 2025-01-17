from collections import defaultdict
from itertools import combinations

with open("input.txt") as f:
    board = f.read().strip().split("\n")
    h = len(board)
    w = len(board[0])

nodes = set()
stations = defaultdict(list)

for row in range(h):
    for col in range(w):
        if board[row][col] != ".":
            stations[board[row][col]].append((col, row))

for key, locations in stations.items():
    comb = combinations(locations, 2)
    for c in comb:
        x1, x2 = c[0][0], c[1][0]
        y1, y2 = c[0][1], c[1][1]
        dx = x2 - x1
        dy = y2 - y1
        i = 0
        while True:
            out = 0
            new_x1, new_x2 = x1 - dx * i, x2 + dx * i
            new_y1, new_y2 = y1 - dy * i, y2 + dy * i
            if 0 <= new_x1 < w and 0 <= new_y1 < h:
                nodes.add((new_x1, new_y1))
            else:
                out += 1
            if 0 <= new_x2 < w and 0 <= new_y2 < h:
                nodes.add((new_x2, new_y2))
            else:
                out += 1
            if out == 2:
                break
            i += 1

print(len(nodes))
