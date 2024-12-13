import re
import numpy as np

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
    prize_x = int(match.groups(1)[0]) + 10000000000000
    match = re.search(r"(?:Y)=(\d+)", prize)
    prize_y = int(match.groups(1)[0]) + 10000000000000

    x, y = np.linalg.solve([(ax, bx), (ay, by)], [(prize_x), (prize_y)])
    a_presses = round(x)
    b_presses = round(y)
    if a_presses * ax + b_presses * bx == prize_x and a_presses * ay + b_presses * by == prize_y:
        ans += 3 * a_presses + b_presses

print(ans)