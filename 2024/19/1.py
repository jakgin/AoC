with open("in") as f:
    parts = f.read().strip().split("\n\n")

towels = set(parts[0].split(", "))
patterns = parts[1].split("\n")

ans = 0

for pattern in patterns:
    i = 0
    j = 1
    sol = []
    unsolvable = set()
    while True:
        # print(sol)
        if i >= len(pattern):
            ans += 1
            break
        if i + j > len(pattern) or i in unsolvable:
            # No solution from here
            if len(sol) == 0:
                break
            unsolvable.add(i)
            last_element = sol.pop()
            i -= len(last_element)
            j = len(last_element) + 1
        if pattern[i:i+j] in towels:
            sol.append(pattern[i:i+j])
            i += j
            j = 1
        else:
            j += 1
    

print(ans)