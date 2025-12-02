package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	zeroCount1 := sol1()
	zeroCount2 := sol2()
	fmt.Println("Zero count in star1 is:", zeroCount1)
	fmt.Println("Zero count in star2 is:", zeroCount2)
}

type dial struct {
	start           int
	countZeroPasses int
}

func newDial() *dial {
	return &dial{50, 0}
}

func (d *dial) rotate(rotation string, amount int) {
	switch rotation {
	case "L":
		d.start -= amount
	case "R":
		d.start += amount
	}

	d.start %= 100
	if d.start < 0 {
		d.start = 100 + d.start
	}
}

func (d *dial) rotateWithCount(rotation string, amount int) {
	laps := amount / 100
	d.countZeroPasses += laps

	amount %= 100

	switch rotation {
	case "L":
		if d.start-amount <= 0 && d.start != 0 {
			d.countZeroPasses++
		}
		d.start -= amount
	case "R":
		d.start += amount
		if d.start > 99 {
			d.countZeroPasses++
		}
	}

	if d.start < 0 {
		d.start = 100 + d.start
	} else {
		d.start %= 100
	}
}

func sol1() (zeroCount int) {
	dial := newDial()

	file, _ := os.ReadFile("in.txt")
	lines := strings.SplitSeq(string(file), "\n")
	for line := range lines {
		rotation := string(line[0])
		amount, _ := strconv.Atoi(line[1:])
		dial.rotate(rotation, amount)
		if dial.start == 0 {
			zeroCount++
		}
	}
	return
}

func sol2() int {
	dial := newDial()

	file, _ := os.ReadFile("in.txt")
	lines := strings.SplitSeq(string(file), "\n")
	for line := range lines {
		rotation := string(line[0])
		amount, _ := strconv.Atoi(line[1:])
		dial.rotateWithCount(rotation, amount)
	}
	return dial.countZeroPasses
}
