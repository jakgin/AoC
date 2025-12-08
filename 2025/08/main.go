package main

import (
	"cmp"
	"fmt"
	"math"
	"os"
	"slices"
	"strconv"
	"strings"
)

func main() {
	boxes := Input("in.txt")
	connections := CreateConnections(boxes)
	slices.SortFunc(connections, func(conn1, conn2 Connection) int {
		return cmp.Compare(conn1.dist, conn2.dist)
	})

	// sol := sol1(connections)
	sol := sol2(boxes, connections)

	fmt.Println(sol)
}

func sol2(boxes []Box, connections []Connection) int {
	desiredCircuitLength := len(boxes)
	circuits := Circuits{}

	for _, conn := range connections {
		circuits.Connect(conn)

		if len(circuits.items) == 1 && len(circuits.items[0]) == desiredCircuitLength {
			return conn.Box1.X * conn.Box2.X
		}
	}

	return 0
}

func sol1(connections []Connection) int {
	circuits := Circuits{}

	for i := range 1000 {
		circuits.Connect(connections[i])
	}

	slices.SortFunc(circuits.items, func(c1, c2 map[Box]struct{}) int {
		return cmp.Compare(len(c2), len(c1))
	})

	sol := 1
	for i := range 3 {
		sol *= len(circuits.items[i])
	}

	return sol
}

type Circuits struct {
	items []map[Box]struct{}
}

func (c *Circuits) Connect(connection Connection) {
	box1 := connection.Box1
	box2 := connection.Box2

	var circuitIndices []int

	for i, circuit := range c.items {
		if _, ok := circuit[box1]; ok {
			circuitIndices = append(circuitIndices, i)
		} else if _, ok := circuit[box2]; ok {
			circuitIndices = append(circuitIndices, i)
		}
	}

	if len(circuitIndices) == 0 {
		c.items = append(c.items, map[Box]struct{}{box1: {}, box2: {}})
	} else if len(circuitIndices) == 1 {
		c.items[circuitIndices[0]][box1] = struct{}{}
		c.items[circuitIndices[0]][box2] = struct{}{}
	} else {
		// Merge 2 circuits
		for box := range c.items[circuitIndices[1]] {
			c.items[circuitIndices[0]][box] = struct{}{}
		}

		c.items[circuitIndices[1]] = c.items[len(c.items)-1]
		c.items = c.items[:len(c.items)-1]
	}
}

type Box struct {
	X, Y, Z int
}

type Connection struct {
	Box1, Box2 Box
	dist       float64
}

func NewConnection(box1, box2 Box) *Connection {
	dist := math.Sqrt(math.Pow(float64(box1.X)-float64(box2.X), 2) + math.Pow(float64(box1.Y)-float64(box2.Y), 2) + math.Pow(float64(box1.Z)-float64(box2.Z), 2))
	return &Connection{
		Box1: box1,
		Box2: box2,
		dist: dist,
	}
}

func CreateConnections(boxes []Box) []Connection {
	connections := make([]Connection, 0, len(boxes)*len(boxes))
	for i := range boxes {
		for j := i + 1; j < len(boxes); j++ {
			connections = append(connections, *NewConnection(boxes[i], boxes[j]))
		}
	}
	return connections
}

func Input(filename string) []Box {
	file, _ := os.ReadFile(filename)
	lines := strings.Split(string(file), "\n")
	boxes := make([]Box, len(lines))
	for i, line := range lines {
		nums := strings.Split(line, ",")
		x, _ := strconv.Atoi(nums[0])
		y, _ := strconv.Atoi(nums[1])
		z, _ := strconv.Atoi(nums[2])
		boxes[i] = Box{x, y, z}
	}
	return boxes
}
