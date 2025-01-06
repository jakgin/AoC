from functools import cache


with open("in") as f:
    parts = f.read().strip().split("\n\n")

towels = set(parts[0].split(", "))
maxlen = max(map(len, towels))
patterns = parts[1].split("\n")


@cache
def num_possibilities(pattern):
    if pattern == "": return 1
    count = 0
    for i in range(min(len(pattern), maxlen) + 1):
        if pattern[:i] in towels:
            count += num_possibilities(pattern[i:])
    return count

print(sum(num_possibilities(pattern) for pattern in patterns))