with open("input.txt") as f:
    board = f.read().split("\n")

def check(x, y):
    if board[y][x] != WORD[0]:
        return 0
    
    count = 0

    directions = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i != 0 or j != 0:
                directions.append((i, j))
    
    for dx, dy in directions:
        for i, letter in enumerate(WORD):
            curr_x = x + dx * i
            curr_y = y + dy * i
            if not (0 <= curr_x < WIDTH and 0 <= curr_y < HEIGHT):
                break
            if board[curr_y][curr_x] != letter:
                break
            if i == len(WORD) - 1:
                count += 1
        
    return count

ans = 0

WORD = "XMAS"
HEIGHT = len(board)
WIDTH =  len(board[0])

for y in range(HEIGHT):
    for x in range(WIDTH):
        ans += check(x, y)

print(ans)