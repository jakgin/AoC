package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	presents, regions := GetInput(os.Args[1])

	sol := sol1(presents, regions)
	fmt.Println(sol)

	// ShowRegions(regions)
}

func sol1(presents []Present, regions []*Region) int {
	sol := 0

	for i, region := range regions {
		fmt.Printf("Region: %d/%d\n", i+1, len(regions))
		if CanPresentsFit(presents, region) {
			sol++
		}
	}

	return sol
}

func CanPresentsFit(presents []Present, region *Region) bool {
	presentsWithRotations := make([][]Present, len(presents))
	for i := range presentsWithRotations {
		presentsWithRotations[i] = presents[i].GetPresentRotations()
	}

	bestPresentId := 0
	bestPresentRotationId := 0
	bestPresentFit := -1
	var location Point

	for true {
		bestPresentFit = -1

		for presentIndex, presentRotations := range presentsWithRotations {
			for presentRotationId, present := range presentRotations {
				if region.presentsToPlace[presentIndex] == 0 {
					break
				}

				for y := range len(region.grid) {
					for x := range len(region.grid[0]) {
						l := Point{x, y}
						presentFit := region.countWalls(present, l)
						if presentFit > bestPresentFit {
							bestPresentFit = presentFit
							bestPresentId = presentIndex
							bestPresentRotationId = presentRotationId
							location = l
						}
					}
				}

			}
		}

		if bestPresentFit == -1 {
			break
		}

		region.placePresent(presentsWithRotations[bestPresentId][bestPresentRotationId], bestPresentId, location)
	}

	for _, presentsNotPlaced := range region.presentsToPlace {
		if presentsNotPlaced != 0 {
			return false
		}
	}

	return true
}

func GetInput(filename string) ([]Present, []*Region) {
	file, _ := os.ReadFile(filename)
	sectors := strings.Split(string(file), "\n\n")
	presentSectors := sectors[:len(sectors)-1]
	regionSector := sectors[len(sectors)-1]
	regionSectors := strings.Split(regionSector, "\n")

	presents := make([]Present, len(presentSectors))
	regions := make([]*Region, len(regionSectors))

	for i, present := range presentSectors {
		lines := strings.Split(present, "\n")
		present := lines[1:]

		presentGrid := make(Present, len(present))
		for j, line := range present {
			presentGrid[j] = []byte(line)
		}
		presents[i] = presentGrid
	}

	for i, sector := range regionSectors {
		sectors := strings.Split(sector, " ")

		dimensions := strings.Split(strings.TrimRight(sectors[0], ":"), "x")
		width, _ := strconv.Atoi(dimensions[0])
		height, _ := strconv.Atoi(dimensions[1])
		grid := make([][]byte, height)
		for rowIndex := range grid {
			row := make([]byte, width)
			for rowIndex := range row {
				row[rowIndex] = EmptyCell
			}
			grid[rowIndex] = row
		}

		presentsToPlace := make([]int, len(sectors[1:]))
		for presentIndex, numberOfPresents := range sectors[1:] {
			n, _ := strconv.Atoi(numberOfPresents)
			presentsToPlace[presentIndex] = n
		}

		regions[i] = &Region{grid, presentsToPlace}
	}

	return presents, regions
}

const PresentCell = '#'
const EmptyCell = '.'

type Present [][]byte

func (p Present) String() string {
	s := strings.Builder{}

	for _, row := range p {
		fmt.Fprintln(&s, string(row))
	}

	return s.String()
}

func (p Present) GetPresentRotations() []Present {
	presents := make([]Present, 4)
	for i := range 4 {
		presents[i] = make(Present, len(p))
		for j := range presents[i] {
			presents[i][j] = make([]byte, len(p[j]))
		}
	}

	for y := range len(p) {
		for x := range len(p[0]) {
			// 0% rotation
			presents[0][y][x] = p[y][x]

			// 90° rotation
			presents[1][x][len(p)-1-y] = p[y][x]

			// 180° rotation
			presents[2][len(p)-1-y][len(p[0])-1-x] = p[y][x]

			// 270° rotation
			presents[3][len(p[0])-1-x][y] = p[y][x]
		}
	}

	return presents
}

func ShowPresents(presents []Present) {
	for _, present := range presents {
		fmt.Println(present)
	}
}

type Region struct {
	grid            [][]byte
	presentsToPlace []int
}

func (r *Region) String() string {
	buf := strings.Builder{}

	for _, row := range r.grid {
		for _, cell := range row {
			buf.WriteByte(cell)
		}
		buf.WriteString("\n")
	}

	fmt.Fprintln(&buf, r.presentsToPlace)

	return buf.String()
}

// Place present on the grid in location. Return false if present can't be put in this location
func (r *Region) placePresent(present Present, presentId int, location Point) bool {
	for y := range len(present) {
		for x := range len(present[0]) {
			if present[y][x] == EmptyCell {
				continue
			}

			gridY := y + location.Y
			gridX := x + location.X

			if gridY >= len(r.grid) || gridX >= len(r.grid[0]) || r.grid[gridY][gridX] == PresentCell {
				return false
			}
		}
	}

	for y := range len(present) {
		for x := range len(present[0]) {
			if present[y][x] == EmptyCell {
				continue
			}

			gridY := y + location.Y
			gridX := x + location.X

			r.grid[gridY][gridX] = present[y][x]
		}
	}

	r.presentsToPlace[presentId]--

	return true
}

// Check how many walls does present touch in specified location, returns -1 if present can't be placed in location
func (r *Region) countWalls(present Present, location Point) int {
	for y := range len(present) {
		for x := range len(present[0]) {
			if present[y][x] == EmptyCell {
				continue
			}

			gridY := y + location.Y
			gridX := x + location.X

			if gridY >= len(r.grid) || gridX >= len(r.grid[0]) || r.grid[gridY][gridX] == PresentCell {
				return -1
			}
		}
	}

	count := 0
	visited := make(map[Point]struct{})

	for y := range len(present) {
		for x := range len(present[0]) {
			if present[y][x] == EmptyCell {
				continue
			}

			gridY := y + location.Y
			gridX := x + location.X

			directions := []Point{
				{-1, 0}, // up
				{1, 0},  // down
				{0, -1}, // left
				{0, 1},  // right
			}

			for _, dir := range directions {
				neighbourY := gridY + dir.Y
				neighbourX := gridX + dir.X

				if _, counted := visited[Point{neighbourX, neighbourY}]; counted {
					continue
				}

				if neighbourY < 0 || neighbourY >= len(r.grid) || neighbourX < 0 || neighbourX >= len(r.grid[0]) {
					count++
					visited[Point{neighbourX, neighbourY}] = struct{}{}
				} else if r.grid[neighbourY][neighbourX] == PresentCell {
					count++
					visited[Point{neighbourX, neighbourY}] = struct{}{}
				}
			}
		}
	}

	return count
}

func ShowRegions(regions []*Region) {
	for _, region := range regions {
		fmt.Println(region)
	}
}

type Point struct {
	X, Y int
}
