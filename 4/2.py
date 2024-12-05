with open("input2.txt") as f:
    lines = f.read().split("\n")

word = "MAS"

def check(x: int, y: int) -> bool:
    if lines[y][x] != "A":
        return False
    
    if lines[y-1][x-1] + lines[y][x] + lines[y+1][x+1] in [word, word[::-1]]:
        if lines[y+1][x-1] + lines[y][x] + lines[y-1][x+1] in [word, word[::-1]]:
            return True

    return False

ans = 0
for y in range(1, len(lines) - 1):
    for x in range(1, len(lines[y]) - 1):
        if check(x, y):
            ans += 1

print(ans)