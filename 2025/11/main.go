package main

import (
	"fmt"
	"os"
	"slices"
	"strings"
)

func main() {
	graph := GetInput("in.txt")
	// sol := NumberOfPaths(graph, "you", "out")
	sol := CountPaths(graph, "you", "out")
	// sol := NumberOfPathsInludingItems(graph, "svr", "out", "dac", "fft")
	// sol := NumberOfPathsInludingItems(graph, "you", "out", "dxj", "dnq")
	fmt.Println(sol)
}

// Consider paths: (start -> a -> b -> end) OR (start -> b -> a -> end)
func NumberOfPathsInludingItems(graph map[string][]string, start, end, a, b string) int {
	paths1 := CountPaths(graph, start, a)
	paths1 *= CountPaths(graph, a, b)
	paths1 *= CountPaths(graph, b, end)

	paths2 := CountPaths(graph, start, b)
	paths2 *= CountPaths(graph, b, a)
	paths2 *= CountPaths(graph, a, end)

	return paths1 + paths2
}

// topological sort and counting
// Pseudocode:
//
// countPaths(G, A, B):
//
//	topo = topologicalSort(G)
//
//	for each vertex v in G:
//	    dp[v] = 0
//
//	dp[A] = 1
//
//	for u in topo:
//	    for each v in outgoingEdges(u):
//	        dp[v] += dp[u]
//
//	return dp[B]
func CountPaths(graph map[string][]string, a, b string) int {

	return 0
}

func nodeIsRepeating(node GraphNode) bool {
	items := map[string]struct{}{}

	for currentNode := &node; currentNode != nil; {
		if _, ok := items[currentNode.item]; ok {
			return true
		} else {
			items[currentNode.item] = struct{}{}
		}

		currentNode = currentNode.prev
	}

	return false
}

func pathContainItems(node GraphNode, items []string) bool {
	countItems := 0

	for currentNode := &node; currentNode != nil; {
		if slices.Contains(items, currentNode.item) {
			countItems++
		}
		currentNode = currentNode.prev
	}

	return countItems == len(items)
}

func NumberOfPaths(graph map[string][]string, start, end string) int {
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

func GetInput(filename string) map[string][]string {
	file, _ := os.ReadFile(filename)
	lines := strings.Split(string(file), "\n")

	graph := map[string][]string{}
	for _, line := range lines {
		items := strings.Split(line, " ")
		key := items[0][:len(items[0])-1]
		graph[key] = items[1:]
	}

	return graph
}

func ShowGraph(graph map[string][]string) {
	for k, v := range graph {
		fmt.Println(k, v)
	}
}

type GraphNode struct {
	item string
	prev *GraphNode
}
