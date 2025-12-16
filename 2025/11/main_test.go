package main

import "testing"

func TestTopologicalSort(t *testing.T) {
	graph := Graph{
		"D": {"G"},
		"F": {"G"},
		"C": {"B", "E", "D"},
		"A": {"B", "C", "D"},
		"G": {},
		"E": {"F", "G"},
		"B": {"F", "D"},
	}

	sortedNodes := TopologicalSort(graph)

	assertXBeforeY(t, sortedNodes, "A", "B")
	assertXBeforeY(t, sortedNodes, "A", "C")
	assertXBeforeY(t, sortedNodes, "A", "D")
	assertXBeforeY(t, sortedNodes, "C", "B")
	assertXBeforeY(t, sortedNodes, "C", "D")
	assertXBeforeY(t, sortedNodes, "B", "D")
	assertXBeforeY(t, sortedNodes, "E", "F")
	assertXBeforeY(t, sortedNodes, "E", "G")
	assertXBeforeY(t, sortedNodes, "D", "G")
}

func assertXBeforeY(t *testing.T, nodes []string, x, y string) {
	t.Helper()

	seenY := false

	for _, node := range nodes {
		if node == x {
			if seenY {
				t.Errorf("Wrong nodes order, %q should be before %q", x, y)
			}
			return
		}

		if node == y {
			seenY = true
		}
	}
}
