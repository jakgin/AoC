import re

with open("input.txt") as f:
    lines = f.read().strip().split("\n")

ans = 0

for line in lines:
    line = re.sub(r"Card \d: ", "", line)
    winning, my = line.split(" | ")
    winning = winning.split()
    my = my.split()
    
    matches = 0
    for wn in winning:
        if wn in my:
            matches += 1
    
    if matches != 0:
        ans += 2 ** (matches - 1)

print(ans)