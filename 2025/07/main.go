package main

import (
	"errors"
	"fmt"
	"os"
	"strings"
)

func main() {
	file, _ := os.ReadFile("in.txt")
	grid := NewGrid(file)
	sol := sol2(grid)
	// grid.Show() // can be used in sol1
	fmt.Println(sol)
}

func (grid Grid) countPaths(point *Point, cache Cache) int {
	v, ok := cache[*point]
	if ok {
		return v
	}

	switch grid[point.y][point.x] {
	case '^':
		var leftCount, rightCount int
		leftPoint, err := point.GetLeftPoint(grid)
		if err == nil {
			leftCount = grid.countPaths(leftPoint, cache)
			cache[*leftPoint] = leftCount
		}
		rightPoint, err := point.GetRightPoint(grid)
		if err == nil {
			rightCount = grid.countPaths(rightPoint, cache)
			cache[*rightPoint] = rightCount
		}
		sum := leftCount + rightCount
		cache[*point] = sum
		return sum
	default:
		nextPoint, err := point.GetBottomPoint(grid)
		if err != nil {
			cache[*point] = 1
			return 1
		}
		return grid.countPaths(nextPoint, cache)
	}
}

func sol2(grid Grid) int {
	cache := Cache{}
	return grid.countPaths(grid.StartingPoint(), cache)
}

func sol1(grid Grid) int {
	sol := 0

	points := map[*Point]struct{}{grid.StartingPoint(): {}}

	for len(points) != 0 {
		nextPoints := map[*Point]struct{}{}

		for point := range points {
			switch grid[point.y][point.x] {
			case 'S':
				nextPoint, _ := point.GetBottomPoint(grid)
				nextPoints[nextPoint] = struct{}{}
			case '.':
				grid[point.y][point.x] = '|'
				nextPoint, err := point.GetBottomPoint(grid)
				if err != nil {
					continue
				}
				nextPoints[nextPoint] = struct{}{}
			case '^':
				sol++
				leftPoint, err := point.GetLeftPoint(grid)
				if err == nil {
					nextPoints[leftPoint] = struct{}{}
				}
				rightPoint, err := point.GetRightPoint(grid)
				if err == nil {
					nextPoints[rightPoint] = struct{}{}
				}
			}
		}

		points = nextPoints
	}

	return sol
}

type Grid [][]byte

func (g Grid) Show() {
	for _, row := range g {
		fmt.Println(string(row))
	}
}

func NewGrid(file []byte) Grid {
	lines := strings.Split(string(file), "\n")
	grid := make([][]byte, len(lines))

	for rowIndex, line := range lines {
		row := []byte(line)
		grid[rowIndex] = row
	}

	return grid
}

func (g Grid) StartingPoint() *Point {
	for x, ch := range g[0] {
		if string(ch) == "S" {
			return &Point{x, 0}
		}
	}
	return nil
}

type Point struct {
	x, y int
}

func (p *Point) GetBottomPoint(grid Grid) (*Point, error) {
	if p.y+1 >= len(grid) {
		return nil, PointOutsideGridError
	}
	return &Point{p.x, p.y + 1}, nil
}

func (p *Point) GetRightPoint(grid Grid) (*Point, error) {
	if p.x+1 >= len(grid[0]) {
		return nil, PointOutsideGridError
	}
	return &Point{p.x + 1, p.y}, nil
}

func (p *Point) GetLeftPoint(grid Grid) (*Point, error) {
	if p.x <= 0 {
		return nil, PointOutsideGridError
	}
	return &Point{p.x - 1, p.y}, nil
}

var PointOutsideGridError = errors.New("Point goes outside of grid")

type Cache map[Point]int
