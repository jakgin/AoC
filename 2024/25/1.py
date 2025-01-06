with open("in") as f:
    parts = f.read().strip().split("\n\n")

locks = []
keys = []

for part in parts:
    el = part.split("\n")
    hashes = []
    for col in range(len(el[0])):
        hashes_in_col = -1
        for row in range(len(el)):
            if el[row][col] == "#":
                hashes_in_col += 1
        hashes.append(hashes_in_col)
    if el[0] == "#" * len(el[0]):
        locks.append(hashes)
    else:
       keys.append(hashes)

ans = 0

for lock in locks:
    for key in keys:
        overlap = False
        for l, k in zip(lock, key):
            if l + k > 5:
                overlap = True
                break
        if not overlap:
            ans += 1

print(ans)
