from collections import defaultdict

# Approaches:
# Linked List - doesn't work - too slow, too much memory
# Recursion - doesn't work - too slow
# Grouping duplicates - works!

with open("in") as f:
    stones = [int(n) for n in f.read().strip().split()]

groups = defaultdict(int)
for stone in stones:
    groups[stone] += 1

for _ in range(75):
    n_groups = defaultdict(int)
    for stone in groups:
        if stone == 0:
            n_groups[1] += groups[0]
        elif len(str(stone)) % 2 == 0:
            left = int(str(stone)[:len(str(stone)) // 2])
            right = int(str(stone)[len(str(stone)) // 2:])
            n_groups[left] += groups[stone]
            n_groups[right] += groups[stone]
        else:
            n_groups[stone * 2024] += groups[stone]
    groups = n_groups

print(sum(groups.values()))
