with open("input2.txt") as f:
    lines = f.read().split("\n")

word = "XMAS"

def check(x: int, y: int) -> int:
    if lines[y][x] != "X":
        return 0
    count = 0
    
    # Check right-left
    if len(lines[y]) >= x+len(word) and lines[y][x:x+len(word)] == word:
        count += 1
    if x - len(word) + 1 >= 0 and lines[y][x-len(word)+1:x+1] == word[::-1]:
        count += 1
    if len(lines) > y + 3 and lines[y+1][x] + lines[y+2][x] + lines[y+3][x] == word[1:]:
        count += 1
    if y - 3 >= 0 and lines[y-1][x] + lines[y-2][x] + lines[y-3][x] == word[1:]:
        count += 1

    # Check diagonal
    if y - 3 >= 0:
        if len(lines[y-3]) > x + 3 and lines[y-1][x+1] + lines[y-2][x+2] + lines[y-3][x+3] == word[1:]:
            count += 1
        if x - 3 >= 0 and lines[y-1][x-1] + lines[y-2][x-2] + lines[y-3][x-3] == word[1:]:
            count += 1
    if len(lines) > y + 3:
        if len(lines[y+3]) > x + 3 and lines[y+1][x+1] + lines[y+2][x+2] + lines[y+3][x+3] == word[1:]:
            count += 1
        if x - 3 >= 0 and lines[y+1][x-1] + lines[y+2][x-2] + lines[y+3][x-3] == word[1:]:
            count += 1
        

    return count

ans = 0

for y in range(len(lines)):
    for x in range(len(lines[y])):
        ans += check(x, y)

print(ans)