import re
import numpy as np


with open("in") as f:
    lines = f.read().strip().split("\n")

w = 101
h = 103


def move(x, y, vx, vy, seconds):
    new_x = (x + seconds * vx) % w
    new_y = (y + seconds * vy) % h
    return new_x, new_y


def display_grid(grid):
    for row in grid:
        for cell in row:
            if cell == 1:
                print("#", end="")
            else:
                print(" ", end="")
        print()
    print()


def is_tree(grid: np.ndarray):
    """Searches the grid using a window that is 1/2 width and height.
    Window moves some cells every time and we checks if half of the robots
    that is present in the grid is in the window. If so that means that
    robots really cluttered in some place, perhaps forming the tree :)"""
    positions = grid.sum()
    window_w = w // 2
    window_h = h // 2
    
    for row in range(0, h // 2, 20):
        for col in range(0, w // 2, 20):        
            s = np.sum(np.ones((window_h, window_w)) * grid[row:row+window_h, col:col+window_w])
            if s > positions / 2:
                return True
    return False


robots = []
for line in lines:
    robots.append([int(n) for n in re.findall(r"-*\d+", line)])

for i in range(1, 100_000):
    print(i)
    grid = np.zeros((h, w))

    for robot in robots:
        x, y, vx, vy = robot
        new_x, new_y = move(x, y, vx, vy, i)
        grid[new_y, new_x] = 1

    if is_tree(grid):
        display_grid(grid)
        print("Fewest seconds:", i)
        break
