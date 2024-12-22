from collections import deque, defaultdict
from tqdm import tqdm


with open("in") as f:
    lines = f.read().strip().split("\n")


def new_secret(secret: int):
    res = secret * 64
    secret ^= res
    secret %= 16777216

    res = secret // 32
    secret ^= res
    secret %= 16777216

    res = secret * 2048
    secret ^= res
    secret %= 16777216

    return secret


changes = defaultdict(int)

for line in tqdm(lines):
    secret = int(line)
    price = int(str(secret)[-1])
    change = deque()
    seen_changes = set()
    for i in range(2000):
        secret = new_secret(secret)
        new_price = int(str(secret)[-1])
        diff = new_price - price
        change.append(diff)
        if len(change) >= 4:
            if len(change) > 4:
                change.popleft()
            change_t = tuple(change)
            if change_t not in seen_changes:
                seen_changes.add(change_t)
                changes[change_t] += new_price
        price = new_price

print(max(changes.values()))
