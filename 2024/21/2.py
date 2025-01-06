import re
from functools import cache
from itertools import permutations
from collections import deque
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


def sub_seq(keypad, ch, start, dirs):
    seq = []
    start = Node(start, None)
    q = deque([start])
    seen = set(start.coords)
    while len(q) > 0:
        node = q.popleft()
        y, x = node.coords
        if keypad[y][x] == ch:
            start_next = Node((y, x), None)
            # Get the sequence
            dirs_m = {(-1, 0): "^", (0, 1): ">", (1, 0): "v", (0, -1): "<"}
            while node.prev is not None:
                y, x = node.coords
                py, px = node.prev.coords
                seq.append(dirs_m[(y - py, x - px)])
                node = node.prev
            seq.reverse()
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
    return seq, start_next


# solve needs a start argument from the last branch
start_positions = {}

@cache
def solve(seq, lvl, dirs, start):
    # lvl 3 or 26
    if lvl == 3:
        return len(seq)
    
    if lvl == 0:
        start = (3, 2)
    else:
        start = start_positions.get((lvl, dirs), (0, 2))

    new_seq = 0
    for ch in seq:
        if lvl == 0:
            s_seq, start_node  = sub_seq(n_keypad, ch, start, dirs)
        else:
            s_seq, start_node = sub_seq(d_keypad, ch, start, dirs)
       
        new_seq += solve(tuple(s_seq), lvl + 1, dirs, start)
    if lvl != 0:
        start_positions[(lvl, dirs)] = start_node.coords
    return new_seq


ans = 0

for code in codes:
    perm_dirs = permutations([(0, 1), (0, -1), (-1, 0), (1, 0)], 4)
    code_score = int(re.findall(r"\d+", code)[0])
    min_seq_len = float("inf")
    for dirs in perm_dirs:
        seq_len = solve(code, 0, dirs, (3, 2))
        min_seq_len = min(min_seq_len, seq_len)
    print(code, min_seq_len)
    ans += min_seq_len * code_score

print(ans)
for val in start_positions.values():
    print(val)

# Not 322854397266226