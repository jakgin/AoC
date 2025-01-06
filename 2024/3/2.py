import re

with open("input.txt") as f:
    line = f.read()

matches = re.findall(r"(?:mul\(([1-9]\d{0,2}),([1-9]\d{0,2})\)|(do\(\)|don't\(\)))", line)

enabled = True
ans = 0

for match in matches:
    if match[2] == "" and enabled:
        ans += int(match[0]) * int(match[1])
    else:
        enabled = match[2] == "do()"

print(ans)


def sol1(line):
    do_matches = re.finditer(r"do\(\)", line)
    dont_matches = re.finditer(r"don't\(\)", line)
    mul_matches = re.finditer(r"mul\(([1-9]\d{0,2}),([1-9]\d{0,2})\)", line)

    can_mul = True
    do_match = next(do_matches, None)
    dont_match = next(dont_matches, None)
    diff = float("inf")

    for match in mul_matches:
        hit_do = False
        while do_match != None and do_match.start() < match.start():
            can_mul = True
            hit_do = True
            diff = match.start() - do_match.start()
            do_match = next(do_matches, None)
        while dont_match != None and dont_match.start() < match.start():
            diff2 = match.start() - dont_match.start()
            if not hit_do or diff2 < diff:
                can_mul = False
            dont_match = next(dont_matches, None)

        if can_mul:
            ans += int(match.group(1)) * int(match.group(2))

    print(ans)
