package main

import "os"

type Moves struct {
	input         []byte
	nextMoveIndex int
}

func GetMoves() Moves {
	file, _ := os.ReadFile("in.txt")
	return Moves{input: file}
}

func (m *Moves) getNextMove() byte {
	move := m.input[m.nextMoveIndex]
	m.nextMoveIndex = (m.nextMoveIndex + 1) % len(m.input)
	return move
}
