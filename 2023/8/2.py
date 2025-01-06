import re


with open("in") as f:
    parts = f.read().strip().split("\n\n")

moves = parts[0]
lookup = {}
where = []
for line in parts[1].split("\n"):
    match = re.search(r"([A-Z0-9]+) = \(([A-Z0-9]+), ([A-Z0-9]+)\)", line)
    key, left, right = match.groups()
    lookup[key] = (left, right)
    if key.endswith("A"):
        where.append((left, right))

ans = 0
i = 0

while True:
    move = moves[i]
    ans += 1
    count_ends_z = 0

    for j, wh in enumerate(where):
        left, right = wh
        if move == "L":
            if left.endswith("Z"):
                count_ends_z += 1
            where[j] = lookup[left]
        else:
            if right.endswith("Z"):
                count_ends_z += 1
            where[j] = lookup[right]
    if count_ends_z == len(where):
        break

    i = (i + 1) % len(moves)


print(ans)