package main

import (
	"fmt"
	"os"
	"strings"
	"time"
)

func main() {
	tStart := time.Now()

	graph := GetInput("in.txt")
	sol1 := CountPaths(graph, "you", "out")
	sol2 := CountPathsInludingItems(graph, "svr", "out", "dac", "fft")

	fmt.Println(time.Since(tStart))

	fmt.Println(sol1)
	fmt.Println(sol2)
}

// Consider paths: (start -> a -> b -> end) OR (start -> b -> a -> end)
func CountPathsInludingItems(graph Graph, start, end, a, b string) int {
	paths1 := CountPaths(graph, start, a)
	paths1 *= CountPaths(graph, a, b)
	paths1 *= CountPaths(graph, b, end)

	paths2 := CountPaths(graph, start, b)
	paths2 *= CountPaths(graph, b, a)
	paths2 *= CountPaths(graph, a, end)

	return paths1 + paths2
}

func CountPaths(graph Graph, a, b string) int {
	sortedNodes := TopologicalSort(graph)

	paths := map[string]int{}
	for node := range graph {
		paths[node] = 0
	}

	paths[a] = 1

	for _, sortedNode := range sortedNodes {
		for _, node := range graph[sortedNode] {
			paths[node] += paths[sortedNode]
		}
	}

	return paths[b]
}

func TopologicalSort(graph Graph) []string {
	connections := map[string]int{}
	for node := range graph {
		connections[node] = 0
	}

	for _, nextNodes := range graph {
		for _, node := range nextNodes {
			connections[node]++
		}
	}

	zeroNodes := make([]string, 0)
	for node, count := range connections {
		if count == 0 {
			zeroNodes = append(zeroNodes, node)
		}
	}

	sortedNodes := make([]string, 0, len(graph))

	for len(zeroNodes) > 0 {
		currentNode := zeroNodes[0]
		zeroNodes = zeroNodes[1:]
		sortedNodes = append(sortedNodes, currentNode)

		for _, neighbor := range graph[currentNode] {
			connections[neighbor]--
			if connections[neighbor] == 0 {
				zeroNodes = append(zeroNodes, neighbor)
			}
		}
	}

	return sortedNodes
}

func NumberOfPaths(graph Graph, start, end string) int {
	paths := 0
	itemsToProcess := []string{start}

	for len(itemsToProcess) != 0 {
		item := itemsToProcess[0]
		itemsToProcess = itemsToProcess[1:]
		if item == end {
			paths++
			continue
		}

		nextItems := graph[item]
		itemsToProcess = append(itemsToProcess, nextItems...)
	}

	return paths
}

func GetInput(filename string) Graph {
	file, _ := os.ReadFile(filename)
	lines := strings.Split(string(file), "\n")

	graph := Graph{}
	for _, line := range lines {
		items := strings.Split(line, " ")
		key := items[0][:len(items[0])-1]
		graph[key] = items[1:]
	}

	return graph
}

func ShowGraph(graph Graph) {
	for k, v := range graph {
		fmt.Println(k, v)
	}
}

type GraphNode struct {
	item string
	prev *GraphNode
}

type Graph map[string][]string
