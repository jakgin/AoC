package main

import (
	"fmt"
	"os"
	"strings"
)

func main() {
	file, _ := os.ReadFile("in.txt")
	grid := NewGrid(file)
	fmt.Println(sol2(grid))
}

func sol2(grid Grid) int {
	sol := 0

	removablePoints := []Point{}

	for true {
		// grid.show()

		for y := 0; y < len(grid); y++ {
			for x := 0; x < len(grid[0]); x++ {
				if grid[y][x] != '@' {
					continue
				}

				point := Point{x, y}

				if grid.isAccessable(point, 3) {
					removablePoints = append(removablePoints, point)
					sol++
				}
			}
		}

		if len(removablePoints) == 0 {
			break
		}

		grid.removePoints(removablePoints)
		removablePoints = []Point{}
	}

	return sol
}

func sol1(grid Grid) int {
	sol := 0

	for y := 0; y < len(grid); y++ {
		for x := 0; x < len(grid[0]); x++ {
			if grid[y][x] != '@' {
				continue
			}
			if grid.isAccessable(Point{x, y}, 3) {
				sol++
			}
		}
	}

	return sol
}

func NewGrid(file []byte) Grid {
	var lines []string = strings.Split(string(file), "\n")
	grid := make([][]byte, len(lines))
	for i, line := range lines {
		grid[i] = []byte(line)

	}
	return grid
}

func (g Grid) removePoints(points []Point) {
	for _, point := range points {
		g[point.y][point.x] = '.'
	}
}

func (g Grid) isAccessable(point Point, maxAdjacent int) bool {
	adjacents := 0

	for y := -1; y <= 1; y++ {
		for x := -1; x <= 1; x++ {
			if x == 0 && y == 0 {
				continue
			}

			point2 := Point{point.x + x, point.y + y}
			if !g.isPointValid(point2) {
				continue
			}

			if g[point2.y][point2.x] == '@' {
				adjacents++
			}
		}
	}

	return adjacents <= maxAdjacent
}

func (g Grid) show() {
	fmt.Print("\n")
	for _, row := range g {
		for _, point := range row {
			fmt.Print(string(point))
		}
		fmt.Print("\n")
	}
	fmt.Print("\n")
}

type Grid [][]byte

func (g Grid) isPointValid(point Point) bool {
	if point.y < 0 || point.y >= len(g) {
		return false
	}
	if point.x < 0 || point.x >= len(g[0]) {
		return false
	}
	return true
}

type Point struct {
	x, y int
}
