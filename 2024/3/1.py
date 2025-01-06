import re

with open("input.txt") as f:
    line = f.read()

matches = re.finditer(r"mul\(([1-9]\d{0,2}),([1-9]\d{0,2})\)", line)
ans = 0

for match in matches:
    ans += int(match.group(1)) * int(match.group(2))

print(ans)
