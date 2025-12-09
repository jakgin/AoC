package main

import "fmt"

// solution based on grid, works only for small grid input
func sol2smallInputGridExample(points []Point) int {
	grid := NewGrid(points)
	grid.Show()

	grid.ConnectRedTiles()
	grid.Show()

	grid.FillCenterWithGreenTiles()
	grid.Show()

	maxArea := 0
	for i := range points {
		for j := i + 1; j < len(points); j++ {
			if !grid.IsRectangleGreen(points[i], points[j]) {
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

type Grid struct {
	Items         [][]byte
	Width, Height int
}

func NewGrid(points []Point) *Grid {
	grid := &Grid{}

	for _, point := range points {
		if point.X > grid.Width {
			grid.Width = point.X
		}
		if point.Y > grid.Height {
			grid.Height = point.Y
		}
	}

	grid.Width += 1
	grid.Height += 1

	grid.Items = make([][]byte, grid.Height)
	for y := range grid.Items {
		grid.Items[y] = make([]byte, grid.Width)
		for x := range grid.Items[y] {
			grid.Items[y][x] = EmptyTile
		}
	}

	for _, point := range points {
		grid.Items[point.Y][point.X] = RedTile
	}

	return grid
}

func (g *Grid) Show() {
	for _, row := range g.Items {
		for _, cell := range row {
			fmt.Print(string(cell))
		}
		fmt.Println()
	}
	fmt.Println()
}

func (g *Grid) ConnectRedTiles() {
	for y := range g.Height {
		for x := range g.Width {
			if g.Items[y][x] != RedTile {
				continue
			}

			directions := []Point{{1, 0}, {0, 1}, {-1, 0}, {0, -1}}
			for _, dir := range directions {
				visitedCells := []Point{}
				nextCell := Point{x, y}
				for true {
					nextCell = Point{nextCell.X + dir.X, nextCell.Y + dir.Y}

					if nextCell.X < 0 || nextCell.X >= g.Width || nextCell.Y < 0 || nextCell.Y >= g.Height {
						break
					}

					if g.Items[nextCell.Y][nextCell.X] != RedTile {
						visitedCells = append(visitedCells, nextCell)
						continue
					}

					for _, cell := range visitedCells {
						g.Items[cell.Y][cell.X] = GreenTile
					}
					break
				}
			}
		}
	}
}

func (g *Grid) FillCenterWithGreenTiles() {
	for y := range g.Height {
		for x := range g.Width {
			if g.Items[y][x] != EmptyTile {
				continue
			}

			cellShouldBeGreen := true
			directions := []Point{{1, 0}, {0, 1}, {-1, 0}, {0, -1}}

			for _, dir := range directions {
				countPassedWalls := 0
				previousCellEmpty := true
				nextCell := Point{x, y}

				for true {
					nextCell = Point{nextCell.X + dir.X, nextCell.Y + dir.Y}

					if nextCell.X < 0 || nextCell.X >= g.Width || nextCell.Y < 0 || nextCell.Y >= g.Height {
						break
					}

					if (g.Items[nextCell.Y][nextCell.X] == RedTile || g.Items[nextCell.Y][nextCell.X] == GreenTile) && previousCellEmpty {
						countPassedWalls++
						previousCellEmpty = false
						continue
					}

					if g.Items[nextCell.Y][nextCell.X] == EmptyTile {
						previousCellEmpty = true
					}
				}

				if countPassedWalls%2 == 0 {
					cellShouldBeGreen = false
					break
				}
			}

			if cellShouldBeGreen {
				g.Items[y][x] = GreenTile
			}

		}
	}
}

func (g *Grid) IsRectangleGreen(p1, p2 Point) bool {
	minX, minY := p1.X, p1.Y
	maxX, maxY := p2.X, p2.Y
	if p2.X < minX {
		minX, maxX = p2.X, p1.X
	}
	if p2.Y < minY {
		minY, maxY = p2.Y, p1.Y
	}

	for y := minY; y <= maxY; y++ {
		for x := minX; x <= maxX; x++ {
			if g.Items[y][x] != GreenTile && g.Items[y][x] != RedTile {
				return false
			}
		}
	}

	return true
}

const EmptyTile = '.'
const RedTile = '#'
const GreenTile = 'X'
