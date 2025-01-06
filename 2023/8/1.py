import re


with open("in") as f:
    parts = f.read().strip().split("\n\n")

moves = parts[0]
lookup = {}
for line in parts[1].split("\n"):
    match = re.search(r"([A-Z]+) = \(([A-Z]+), ([A-Z]+)\)", line)
    key, left, right = match.groups()
    lookup[key] = (left, right)

ans = 0
i = 0
where = lookup["AAA"]

while True:
    move = moves[i]
    ans += 1

    left, right = where
    if move == "L":
        if left == "ZZZ":
            break
        where = lookup[left]
    else:
        if right == "ZZZ":
            break
        where = lookup[right]

    i = (i + 1) % len(moves)
    
print(ans)