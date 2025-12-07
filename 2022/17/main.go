package main

import (
	"fmt"
)

func main() {
	moves := GetMoves()
	grid := NewGrid()

	for range 200_000 {
		grid.PlaceNewRock()

		for grid.IsRockMoving() {
			move := moves.getNextMove()
			grid.MoveRock(move)
		}
	}

	sol := grid.HighestPointY + 1
	fmt.Println(sol)
}
