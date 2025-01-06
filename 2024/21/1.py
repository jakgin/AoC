import re
from collections import deque
from itertools import permutations
from copy import copy


with open("in") as f:
    codes = f.read().strip().split("\n")

n_keypad = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    [" ", "0", "A"]
]

d_keypad = [
    [" ", "^", "A"],
    ["<", "v", ">"]
]


class Node:
    def __init__(self, coords, prev):
        self.coords = coords
        self.prev = prev


def solve(keypad, code, dirs):
    for y in range(len(keypad)):
        for x in range(len(keypad[0])):
            if keypad[y][x] == "A":
                start = Node((y, x), None)

    seq = []
    for ch in code:
        q = deque([start])
        seen = set(start.coords)
        while len(q) > 0:
            node = q.popleft()
            y, x = node.coords
            if keypad[y][x] == ch:
                start = Node((y, x), None)
                # Get the sequence
                dirs_m = {(-1, 0): "^", (0, 1): ">", (1, 0): "v", (0, -1): "<"}
                sub_seq = []
                while node.prev is not None:
                    y, x = node.coords
                    py, px = node.prev.coords
                    sub_seq.append(dirs_m[(y - py, x - px)])
                    node = node.prev
                seq += reversed(sub_seq)
                seq.append("A")
                break

            c_dirs = list(copy(dirs))
            if node.prev:
                # Prioritize first adding same as last direction neighbor
                dy = node.coords[0] - node.prev.coords[0]
                dx = node.coords[1] - node.prev.coords[1]
                c_dirs.remove((dy, dx))
                c_dirs.insert(0, (dy, dx))
            for dy, dx in c_dirs:
                ny, nx = y + dy, x + dx
                if 0 <= ny < len(keypad) and 0 <= nx < len(keypad[0]):
                    if keypad[ny][nx] != " " and (ny, nx) not in seen:
                        seen.add((ny, nx))
                        q.append(Node((ny, nx), node))
        
    return seq


ans = 0
for code in codes:
    print(code)
    dirs = [(0, 1), (0, -1), (-1, 0), (1, 0)]
    perm = permutations(dirs, 4)
    min_seq = []
    seq = []
    for dirs in perm:
        seq = solve(n_keypad, code, dirs)
        for _ in range(2):
            seq =  solve(d_keypad, seq, dirs)
        if min_seq == [] or len(seq) < len(min_seq):
            min_seq = seq
    print("".join(min_seq))
    print(len(min_seq))
    ans += len(min_seq) * int(re.findall(r"\d+", code)[0])

print(ans)