from functools import cache

with open("in") as f:
    stones = [int(n) for n in f.read().strip().split()]


# Dynamic Programming approach

@cache
def count_stones(stone, lvl):
    if lvl == 75:
        return 1
    
    count = 0
    if stone == 0:
        count += count_stones(1, lvl + 1)
    elif len(str(stone)) % 2 == 0:
        left = int(str(stone)[:len(str(stone)) // 2])
        right = int(str(stone)[len(str(stone)) // 2:])
        count += count_stones(left, lvl + 1)
        count += count_stones(right, lvl + 1)
    else:
        count += count_stones(2024 * stone, lvl + 1)

    return count


ans = 0
for stone in stones:
    ans += count_stones(stone, 0)

print(ans)