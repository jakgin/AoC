import time


def main():
    grid = get_grid()
    t = time.time()
    sol = count_paths(grid, starting_point(grid), {})
    t2 = time.time()

    print(f"Time: {t2 - t:.6f} seconds")  # Python is 5 times slower than Go here
    print(sol)


def count_paths(grid, point: tuple[int, int], cache: dict) -> int:
    if point in cache:
        return cache[point]

    if grid[point[1]][point[0]] == "^":
        left = (point[0] - 1, point[1])
        left_v = count_paths(grid, left, cache)
        cache[left] = left_v

        right = (point[0] + 1, point[1])
        right_v = count_paths(grid, right, cache)
        cache[right] = right_v

        total = left_v + right_v
        cache[point] = total
        return total
    else:
        if len(grid) <= point[1] + 1:
            cache[point] = 1
            return 1
        bottom = (point[0], point[1] + 1)
        return count_paths(grid, bottom, cache)


def get_grid() -> list[list[str]]:
    grid = []
    with open("in.txt") as file:
        for line in file:
            grid.append([x for x in line.strip()])
    return grid


def starting_point(grid: list[list[str]]) -> tuple[int, int]:
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == "S":
                return (x, y)
    raise ValueError("No starting point found")


if __name__ == "__main__":
    main()
