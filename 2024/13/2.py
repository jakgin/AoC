import re
import numpy as np

with open("in") as f:
    ins = f.read().strip().split("\n\n")

ans = 0


def get_numbers(s: str):
    return [int(num) for num in re.findall(r"\d+", s)]


for machine in ins:
    a, b, prize = machine.split("\n")
    ax, ay = get_numbers(a)
    bx, by = get_numbers(b)
    prize_x, prize_y = get_numbers(prize)
    prize_x += 10000000000000
    prize_y += 10000000000000

    x, y = np.linalg.solve([(ax, bx), (ay, by)], [(prize_x), (prize_y)])
    a_presses = round(x)
    b_presses = round(y)
    if (
        a_presses * ax + b_presses * bx == prize_x
        and a_presses * ay + b_presses * by == prize_y
    ):
        ans += 3 * a_presses + b_presses

print(ans)
