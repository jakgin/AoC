with open("input.txt") as f:
    grid = f.read().strip().split("\n")
    h = len(grid)
    w = len(grid[0])

directions = []
for i in range(-1, 2):
    for j in range(-1, 2):
        if (i, j) != (0, 0):
            directions.append((i, j))

def connects(row, col):
    for d in directions:
        n_row = row + d[0]
        n_col = col + d[1]
        if not (0 <= n_row < h and 0 <= n_col < w):
            continue
        if grid[n_row][n_col] != "." and not grid[n_row][n_col].isdigit():
            return True
    return False
        
def hole_number(row, col):
    num = []
    i = 0
    while True:
        i += 1
        if not 0 <= col - i:
            break
        val = grid[row][col - i]
        if val.isdigit():
            num.append(val)
            seen.add((row, col - i))
        else:
            break
    num.reverse()
    num.append(grid[row][col])
    seen.add((row, col))
    i = 0
    while True:
        i += 1
        if not col + i < w:
            break
        val = grid[row][col + i]
        if val.isdigit():
            num.append(val)
            seen.add((row, col + i))
        else:
            break
    return int("".join(num))

ans = 0
seen = set()

for row in range(h):
    for col in range(w):
        if grid[row][col].isdigit() and not (row, col) in seen:
            if connects(row, col):
                ans += hole_number(row, col)

print(ans)