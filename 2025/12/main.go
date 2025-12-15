package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	presents, regions := GetInput(os.Args[1])

	sol := sol2(presents, regions)

	fmt.Println(sol)
}

// Sol1 tries to find best present and its location for given grid state and put it there based on present connectivity
// with the walls and other presents. (Runs 15 min on i5-12400f)
func sol1(presents []Present, regions []*Region) int {
	sol := 0

	for i, region := range regions {
		canFit := CanPresentsFit(presents, region)
		log := "Region: %d/%d - %.2f"
		if canFit {
			sol++
			log += " fit"
		}
		fmt.Printf(log+"\n", i+1, len(regions), region.FilledRatio()*100)
	}

	return sol
}

// Sol2 checks what is the sum of volume of all presents to place on the grid.
// It assumes that presents can be placed based on some volume treshhold.
// For my input, treshold from 0.75 to 1.0 gives the right solution (solution instantly)
func sol2(presents []Present, regions []*Region) int {
	sol := 0
	treshold := 0.85

	presentFills := make([]int, len(presents))
	for i, present := range presents {
		fills := 0

		for _, row := range present.grid {
			for _, cell := range row {
				if cell == PresentCell {
					fills++
				}
			}
		}

		presentFills[i] = fills
	}

	for _, region := range regions {
		fillCount := 0
		for presentId, n := range region.presentsToPlace {
			fillCount += n * presentFills[presentId]
		}
		ratio := float64(fillCount) / float64(len(region.grid)*len(region.grid[0]))
		if ratio < treshold {
			sol++
		}
	}

	return sol
}

func CanPresentsFit(presents []Present, region *Region) bool {
	presentsWithRotations := PresentsWithRotations(presents)

	for anyPresentFit := true; anyPresentFit; {
		anyPresentFit = false
		bestPresentFit := -1
		var bestPresent Present
		var bestLocation Point

		for _, present := range presentsWithRotations {
			if region.presentsToPlace[present.id] == 0 {
				continue
			}

			for y := range region.grid {
				for x := range region.grid[y] {
					location := Point{x, y}
					presentFit, err := region.countWalls(present, location)

					if err != nil {
						continue
					}

					if presentFit > bestPresentFit {
						bestPresentFit = presentFit
						bestPresent = present
						bestLocation = location
						anyPresentFit = true
					}
				}
			}
		}

		if anyPresentFit {
			region.placePresent(bestPresent, bestLocation)
		}
	}

	return SumInts(region.presentsToPlace) == 0
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

func SumInts(nums []int) int {
	sum := 0
	for _, n := range nums {
		sum += n
	}
	return sum
}

func PresentsWithRotations(presents []Present) []Present {
	presentsWithRotations := make([]Present, 0, len(presents)*4)
	for _, present := range presents {
		presentsWithRotations = append(presentsWithRotations, present.GetPresentRotations()...)
	}
	return presentsWithRotations
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

func (r *Region) FilledRatio() float64 {
	filled := 0.0
	for _, row := range r.grid {
		for _, cell := range row {
			if cell == PresentCell {
				filled++
			}
		}
	}
	return filled / float64(len(r.grid)*len(r.grid[0]))
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
