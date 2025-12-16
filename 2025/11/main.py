from collections import defaultdict, deque
from time import time


def main():
    t1 = time()

    graph = get_input("in.txt")
    sol1 = count_paths(graph, "you", "out")
    sol2 = count_paths_including_items(graph, "svr", "out", "dac", "fft")

    t2 = time()

    print(f"Time: {((t2 - t1) * 1000):.6f} seconds")

    print(sol1)
    print(sol2)


def topological_sort(graph: dict[str, list[str]]) -> list[str]:
    in_degree = defaultdict(int)
    for u in graph:
        for v in graph[u]:
            in_degree[v] += 1

    zero_in_degree = deque([u for u in graph if in_degree[u] == 0])
    sorted_list = []

    while zero_in_degree:
        u = zero_in_degree.popleft()
        sorted_list.append(u)
        for v in graph[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                zero_in_degree.append(v)

    if len(sorted_list) != len(graph):
        raise ValueError("Graph has at least one cycle")

    return sorted_list


def count_paths(graph: dict[str, list[str]], a: str, b: str) -> int:
    sorted_nodes = topological_sort(graph)

    paths = {node: 0 for node in graph}
    paths[a] = 1

    for sorted_node in sorted_nodes:
        for node in graph[sorted_node]:
            paths[node] += paths[sorted_node]

    return paths[b]


def count_paths_including_items(
    graph: dict[str, list[str]], start: str, end: str, a: str, b: str
) -> int:
    paths1 = count_paths(graph, start, a)
    paths1 *= count_paths(graph, a, b)
    paths1 *= count_paths(graph, b, end)

    paths2 = count_paths(graph, start, b)
    paths2 *= count_paths(graph, b, a)
    paths2 *= count_paths(graph, a, end)

    return paths1 + paths2


def get_input(filename: str) -> dict[str, list[str]]:
    graph = defaultdict(list)
    with open(filename) as f:
        for line in f:
            items = line.strip().split(" ")
            graph[items[0][:-1]] = items[1:]
    return graph


if __name__ == "__main__":
    main()
