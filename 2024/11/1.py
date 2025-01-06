with open("in") as f:
    stones = [int(n) for n in f.read().strip().split()]

for _ in range(25):
    i = 0
    while i < len(stones):
        if stones[i] == 0:
            stones[i] = 1
        elif len(str(stones[i])) % 2 == 0:
            left = int(str(stones[i])[:len(str(stones[i])) // 2])
            right = int(str(stones[i])[len(str(stones[i])) // 2:])
            stones[i] = left
            stones.insert(i + 1, right)
            i += 1
        else:
            stones[i] *= 2024
        i += 1

print(len(stones))