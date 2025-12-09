package main

import (
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
)

func main() {
	points := GetInput("in.txt")
	sol := sol2(points)
	fmt.Println(sol)
}

func sol1(points []Point) int {
	maxArea := 0

	for i := range points {
		for j := i + 1; j < len(points); j++ {
			area := RectangleArea(points[i], points[j])
			if area > maxArea {
				maxArea = area
			}
		}
	}

	return maxArea
}

// Idea: Get edges and check for every rectangle if there is an edge inside rectangle. If not then it is green.
// sol=1525207666 too low
func sol2(points []Point) int {
	maxArea := 0
	boundries := BoundriesFromPoints(points)

	for i := range points {
		for j := i + 1; j < len(points); j++ {
			rectBoundry := BoundryFromPoints(points[i], points[j])
			if Intersect(boundries, rectBoundry) {
				continue
			}

			area := RectangleArea(points[i], points[j])
			if area > maxArea {
				maxArea = area
			}
		}
	}

	return maxArea
}

func GetInput(filename string) []Point {
	file, _ := os.ReadFile(filename)
	lines := strings.Split(string(file), "\n")
	points := make([]Point, len(lines))

	for i, line := range lines {
		coords := strings.Split(line, ",")
		x, _ := strconv.Atoi(coords[0])
		y, _ := strconv.Atoi(coords[1])
		point := Point{x, y}
		points[i] = point
	}

	return points
}

func BoundriesFromPoints(points []Point) []Boundry {
	boundries := make([]Boundry, len(points))

	horizontal := true
	for i, point := range points {
		for j, point2 := range points {
			if horizontal && point.Y != point2.Y {
				continue
			}

			if !horizontal && point.X != point2.X {
				continue
			}

			if i == j {
				continue
			}

			boundries[i] = BoundryFromPoints(point, point2)
			horizontal = !horizontal
			break
		}
	}

	return boundries
}

// Rectangle is green if there is no inner intersection of any boundry created by edge with rectangle
func Intersect(boundries []Boundry, rect Boundry) bool {
	for _, boundry := range boundries {
		if boundry.MinY < rect.MaxY && boundry.MaxY > rect.MinY && boundry.MinX < rect.MaxX && boundry.MaxX > rect.MinX {
			return true
		}
	}

	return false
}

func RectangleArea(p1 Point, p2 Point) int {
	return int(math.Abs(float64(p1.X-p2.X+1)) * math.Abs(float64(p1.Y-p2.Y+1)))
}

type Point struct {
	X, Y int
}

type Boundry struct {
	MinX, MaxX, MinY, MaxY int
}

func BoundryFromPoints(p1, p2 Point) Boundry {
	minX, minY := p1.X, p1.Y
	maxX, maxY := p2.X, p2.Y
	if p2.X < minX {
		minX, maxX = p2.X, p1.X
	}
	if p2.Y < minY {
		minY, maxY = p2.Y, p1.Y
	}
	return Boundry{
		MinX: minX,
		MaxX: maxX,
		MinY: minY,
		MaxY: maxY,
	}
}
