with open("input.txt") as f:
    rules, updates = f.read().strip().split("\n\n")
    rules = [rule.split("|") for rule in rules.split("\n")]
    updates = [update.split(",") for update in updates.split("\n")]

def follows_rules(update):
    idx = {}
    for i, num in enumerate(update):
        idx[num] = i

    for a, b in rules:
        if a in idx and b in idx and not idx[a] < idx[b]:
            return False

    return True

ans = 0

for update in updates:
    if follows_rules(update):
        ans += int(update[len(update) // 2])

print(ans)
