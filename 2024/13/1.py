import re

with open("in") as f:
    ins = f.read().strip().split("\n\n")


def get_numbers(s: str):
    return [int(num) for num in re.findall(r"\d+", s)]


ans = 0

for machine in ins:
    a, b, prize = machine.split("\n")
    ax, ay = get_numbers(a)
    bx, by = get_numbers(b)
    prize_x, prize_y = get_numbers(prize)

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
