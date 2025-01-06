with open("input.txt") as f:
    rules, updates = f.read().strip().split("\n\n")
    rules = [rule.split("|") for rule in rules.split("\n")]
    updates = [update.split(",") for update in updates.split("\n")]

def fix_update(update: list[str]):
    idx = {}
    for i, num in enumerate(update):
        idx[num] = i

    need_fix = False

    while True:
        follows_rules = True
        for a, b in rules:
            if a in idx and b in idx and not idx[a] < idx[b]:
                follows_rules = False
                need_fix = True
                update.insert(idx[b], a)
                update.pop(idx[a] + 1)
                for i, num in enumerate(update):
                    idx[num] = i
        if follows_rules:
            break

    if need_fix:
        return int(update[len(update) // 2])
    return 0

ans = 0

for update in updates:
    ans += fix_update(update)

print(ans)
