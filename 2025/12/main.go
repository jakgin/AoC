package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	sol := 0
	presents, regions := GetInput(os.Args[1])

	for i, region := range regions {
		canFit := CanPresentsFit(presents, region)
		log := "Region: %d/%d"
		if canFit {
			sol++
			log += " fit"
		}
		fmt.Printf(log+"\n", i+1, len(regions))
	}

	fmt.Println(sol)
}

// TODO: Optimization: keep track of the squares to check in a grid (only those that connect to wall or another present)
func CanPresentsFit(presents []Present, region *Region) bool {
	presentsWithRotations := make([][]Present, len(presents))
	for i := range presentsWithRotations {
		presentsWithRotations[i] = presents[i].GetPresentRotations()
	}

	for true {
		noPresentFit := true
		bestPresentFit := -1
		var bestPresent Present
		var location Point

		for presentIndex, presentRotations := range presentsWithRotations {
			for _, present := range presentRotations {
				if region.presentsToPlace[presentIndex] == 0 {
					break
				}

				for y := range len(region.grid) {
					for x := range len(region.grid[0]) {
						l := Point{x, y}
						presentFit, err := region.countWalls(present, l)

						if err != nil {
							continue
						}

						if presentFit > bestPresentFit {
							bestPresentFit = presentFit
							bestPresent = present
							location = l
							noPresentFit = false
						}
					}
				}

			}
		}

		if noPresentFit {
			break
		}

		region.placePresent(bestPresent, location)
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

		presentGrid := make(Grid, len(present))
		for j, line := range present {
			presentGrid[j] = []byte(line)
		}
		presents[i] = Present{id: i, grid: presentGrid}
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

type Present struct {
	id   int
	grid Grid
}

func (p Present) String() string {
	s := strings.Builder{}

	fmt.Fprintf(&s, "Id: %d\n", p.id)
	for _, row := range p.grid {
		fmt.Fprintln(&s, string(row))
	}

	return s.String()
}

func (p Present) GetPresentRotations() []Present {
	presents := make([]Present, 4)

	for i := range 4 {
		grid := make(Grid, len(p.grid))
		for rowI := range grid {
			grid[rowI] = make([]byte, len(p.grid[rowI]))
		}
		presents[i] = Present{p.id, grid}
	}

	for y := range len(p.grid) {
		for x := range len(p.grid[y]) {
			// 0% rotation
			presents[0].grid[y][x] = p.grid[y][x]

			// 90° rotation
			presents[1].grid[x][len(p.grid)-1-y] = p.grid[y][x]

			// 180° rotation
			presents[2].grid[len(p.grid)-1-y][len(p.grid[0])-1-x] = p.grid[y][x]

			// 270° rotation
			presents[3].grid[len(p.grid[0])-1-x][y] = p.grid[y][x]
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
	grid            Grid
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

func (r *Region) canPlacePresent(present Present, location Point) bool {
	for y := range len(present.grid) {
		for x := range len(present.grid[y]) {
			if present.grid[y][x] == EmptyCell {
				continue
			}

			gridY := y + location.Y
			gridX := x + location.X

			if gridY >= len(r.grid) || gridX >= len(r.grid[0]) || r.grid[gridY][gridX] == PresentCell {
				return false
			}
		}
	}

	return true
}

// Place present on the grid in specified location. Return an error if present can't be placed
func (r *Region) placePresent(present Present, location Point) error {
	if !r.canPlacePresent(present, location) {
		return fmt.Errorf("Present can't be put in location %v", location)
	}

	for y := range len(present.grid) {
		for x := range len(present.grid[y]) {
			if present.grid[y][x] == EmptyCell {
				continue
			}

			gridY := y + location.Y
			gridX := x + location.X

			r.grid[gridY][gridX] = present.grid[y][x]
		}
	}

	r.presentsToPlace[present.id]--

	return nil
}

// Check how many walls does present touch in specified location, returns error if present can't be placed there
func (r *Region) countWalls(present Present, location Point) (int, error) {
	if !r.canPlacePresent(present, location) {
		return 0, fmt.Errorf("Present can't be put in location %v", location)
	}

	count := 0
	visited := make(map[Point]struct{})

	for y := range len(present.grid) {
		for x := range len(present.grid[y]) {
			if present.grid[y][x] == EmptyCell {
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

	return count, nil
}

func ShowRegions(regions []*Region) {
	for _, region := range regions {
		fmt.Println(region)
	}
}

type Point struct {
	X, Y int
}

type Grid [][]byte
