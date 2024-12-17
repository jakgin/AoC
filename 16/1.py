import heapq
from copy import copy
from print_color import print as pprint


with open("in") as f:
    lines = f.read().strip().split("\n")


def main():
    grid, start_node = build_grid(lines)
    end_node = shortest_path(grid, start_node)
    assert end_node != None
    display_path(grid, end_node)
    print(end_node.cost)


class Node:
    def __init__(self, val, coords, dir, cost=float("inf"), prev=None):
        self.val = val
        self.coords = coords
        self.dir = dir
        self.cost = cost
        self.prev = prev
    
    def __str__(self):
        return self.val
    
    def __lt__(self, other):
        return self.cost < other.cost


def build_grid(lines):
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    grid = []
    for i, line in enumerate(lines):
        row = []
        for j, cell in enumerate(line):
            if cell in [".", "E"]:
                row.append([Node(cell, (i, j), d) for d in dirs])
            elif cell == "S":
                start = Node(cell, (i, j), (0, 1), cost=0)
                row.append([Node(cell, (i, j), d) for d in dirs[1:]] + [start])
            else:
                row.append(cell)
        grid.append(row)
    return grid, start


def show_grid(grid):
    for row in grid:
        for cell in row:
            if type(cell) == list:
                print(cell[0].val, end="")
            else:
                print(cell, end="")
        print()


def valid_neighbors(grid, node):
    y, x = node.coords
    nbs = []

    ny, nx = y + node.dir[0], x + node.dir[1]
    nodes = grid[ny][nx]
    if type(nodes) == list:
        for n_node in nodes:
            if n_node.dir == node.dir:
                if node.cost + 1 < n_node.cost:
                    n_node.cost = node.cost + 1
                    n_node.prev = node
                    nbs.append(n_node)
                    break
    for n_node in grid[y][x]:
        if n_node.dir == node.dir:
            continue
        if node.cost + 1000 < n_node.cost:
            n_node.cost = node.cost + 1000
            n_node.prev = node
            nbs.append(n_node)
    return nbs


def shortest_path(grid, start_node):
    pq = [start_node]
    heapq.heapify(pq)
    while len(pq) > 0:
        node = heapq.heappop(pq)
        if node.val == "E":
            return node
        nbs = valid_neighbors(grid, node)
        for nb in nbs:
            heapq.heappush(pq, nb)
    return None


def display_path(grid, end_v):
    s_grid = copy(grid)
    while end_v.prev.val != "S":
        prev = end_v.prev
        prev_y, prev_x = prev.coords
        s_grid[prev_y][prev_x] = "O"
        end_v = end_v.prev
    for row in s_grid:
        for cell in row:
            if cell == "O":
                pprint(cell, color="green", end="")
            elif type(cell) == list:
                print(cell[0].val, end="")
            else:
                print(cell, end="")
        print()


if __name__ == "__main__":
    main()
