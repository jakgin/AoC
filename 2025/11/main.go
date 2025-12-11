package main

import (
	"fmt"
	"os"
	"slices"
	"strings"
)

func main() {
	graph := GetInput("in.txt")
	// sol1 := NumberOfPaths(graph, "you", "out")
	sol2 := NumberOfPathsInludingItems(graph, "svr", "out", []string{"dac", "fft"})
	fmt.Println(sol2)
}

func NumberOfPathsInludingItems(graph map[string][]string, start, end string, items []string) int {
	paths := 0
	nodesToProcess := []GraphNode{{start, nil}}

	for len(nodesToProcess) != 0 {
		node := nodesToProcess[0]
		fmt.Println("Considering node:", node)
		nodesToProcess = nodesToProcess[1:]

		if node.item == end {
			if pathContainItems(node, items) {
				paths++
			}
			continue
		}

		if nodeIsRepeating(node) {
			fmt.Println("node is repeating")
			continue
		}

		nextItems := graph[node.item]
		for _, nextItem := range nextItems {
			nodesToProcess = append(nodesToProcess, GraphNode{nextItem, &node})
		}
	}

	return paths
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
