import re

with open("in") as f:
    ins = f.read().strip().split("\n\n")

ans = 0

for machine in ins:
    a, b, prize = machine.split("\n")
    match = re.search(r"(?:X)\+(\d+)", a)
    ax = int(match.groups(1)[0])
    match = re.search(r"(?:Y)\+(\d+)", a)
    ay = int(match.groups(1)[0])

    match = re.search(r"(?:X)\+(\d+)", b)
    bx = int(match.groups(1)[0])
    match = re.search(r"(?:Y)\+(\d+)", b)
    by = int(match.groups(1)[0])

    match = re.search(r"(?:X)=(\d+)", prize)
    prize_x = int(match.groups(1)[0])
    match = re.search(r"(?:Y)=(\d+)", prize)
    prize_y = int(match.groups(1)[0])

    min_cost = float("inf")
    for ops in range(202):
        for a_presses in range(ops + 1):
            b_presses = ops - a_presses
            start_x = ax * a_presses + bx * b_presses
            start_y = ay * a_presses + by * b_presses

            if start_x == prize_x and start_y == prize_y:
                cost = a_presses * 3 + b_presses
                min_cost = min(min_cost, cost)
    
    if min_cost != float("inf"):
        ans += min_cost

print(ans)