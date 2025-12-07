package main

import "fmt"

type Grid struct {
	Board         [][]byte
	HighestPointY int
	NextRockIndex int
	MovingRock    Rock
	cutPoint      int
}

func NewGrid() *Grid {
	board := make([][]byte, 20_000)
	for i := range 20_000 {
		board[i] = make([]byte, 7)
		for j := range board[i] {
			board[i][j] = '.'
		}
	}
	return &Grid{Board: board, HighestPointY: -1}
}

func (g *Grid) IsRockMoving() bool {
	return g.MovingRock != nil
}

func (g *Grid) MoveRock(direction byte) {
	g.pushMovingRock(direction)

	if g.movingRockCanFall() {
		g.MovingRock = g.MovingRock.RockAfterFall()
	} else {
		g.stopMovingRock()
	}
}

func (g *Grid) PlaceNewRock() {
	rock := g.getNextRock()
	g.placeRock(rock)
}

func (g *Grid) stopMovingRock() {
	for _, point := range g.MovingRock {
		g.Board[point.y-g.cutPoint][point.x-g.cutPoint] = '#'

		if point.y > g.HighestPointY {
			g.HighestPointY = point.y
		}
	}
	g.MovingRock = nil
}

func (g *Grid) cutOffBoard() {
	// Moving top half of the board to the bottom
	for i := range 10_000 {
		g.Board[i] = g.Board[i+10_000]
	}

	// Cleaning top part of the board
	for i := 10_000; i < 20_000; i++ {
		for j := range 7 {
			g.Board[i][j] = '.'
		}
	}

	g.cutPoint += 10_000
}

// push moving rock left or right ('<' or '>') if possible
func (g *Grid) pushMovingRock(direction byte) {
	for _, point := range g.MovingRock {
		var newX int
		switch direction {
		case '<':
			newX = point.x - 1
		case '>':
			newX = point.x + 1
		}

		fmt.Println(point.y, g.cutPoint)
		if newX < 0 || newX >= 7 || g.Board[point.y-g.cutPoint][newX] != '.' {
			return
		}
	}

	for i := range g.MovingRock {
		switch direction {
		case '<':
			g.MovingRock[i].x -= 1
		case '>':
			g.MovingRock[i].x += 1
		}
	}
}

// Place element on the grid in the right place (2 from left, 3 from bottom/last rock)
func (g *Grid) placeRock(rock Rock) {
	staringX := 2
	startingY := g.HighestPointY + 4

	if startingY >= g.cutPoint+19_990 {
		g.cutOffBoard()
	}

	g.MovingRock = make(Rock, len(rock))

	for i, point := range rock {
		g.MovingRock[i] = Point{staringX + point.x, startingY + point.y}
	}
}

func (g *Grid) movingRockCanFall() bool {
	rockAfterFall := g.MovingRock.RockAfterFall()
	for _, point := range rockAfterFall {
		if point.y < 0 {
			return false
		}
		if g.Board[point.y][point.x] == '#' {
			return false
		}
	}
	return true
}

func (g *Grid) getNextRock() Rock {
	rock := Rocks[g.NextRockIndex]
	g.NextRockIndex = (g.NextRockIndex + 1) % len(Rocks)
	return rock
}

var Rocks = []Rock{
	{
		{0, 0},
		{1, 0},
		{2, 0},
		{3, 0},
	},
	{
		{1, 0},
		{0, 1},
		{1, 1},
		{2, 1},
		{1, 2},
	},
	{
		{2, 2},
		{2, 1},
		{2, 0},
		{0, 0},
		{1, 0},
	},
	{
		{0, 0},
		{0, 1},
		{0, 2},
		{0, 3},
	},
	{
		{0, 0},
		{0, 1},
		{1, 0},
		{1, 1},
	},
}

type Point struct {
	x, y int
}

type Rock []Point

func (r Rock) RockAfterFall() Rock {
	newRock := make(Rock, len(r))
	for i, point := range r {
		newRock[i] = Point{point.x, point.y - 1}
	}
	return newRock
}
