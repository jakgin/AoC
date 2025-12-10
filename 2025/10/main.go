package main

import (
	"bytes"
	"fmt"
	"os"
	"strconv"
	"strings"

	"github.com/mxschmitt/golang-combinations"
)

func main() {
	input := GetInput("in.txt")
	sol := sol1(input)
	fmt.Println(sol)
}

func sol1(lines Lines) int {
	sol := 0

	for _, line := range lines {
		sol += FewestButtonPresses(line)
	}

	return sol
}

func FewestButtonPresses(line *Line) int {
	fewest := 1000

	buttonCombinations := combinations.All(line.buttons)
	for _, combination := range buttonCombinations {
		if willLight(combination, line.lights) && len(combination) < fewest {
			fewest = len(combination)
		}
	}

	return fewest
}

func willLight(buttonSequence [][]int, desiredLights []byte) bool {
	lights := emptyLights(len(desiredLights))

	for _, button := range buttonSequence {
		for _, n := range button {
			if lights[n] == '.' {
				lights[n] = '#'
			} else {
				lights[n] = '.'
			}
		}
	}

	return bytes.Equal(lights, desiredLights)
}

func emptyLights(length int) []byte {
	lights := make([]byte, length)
	for i := range lights {
		lights[i] = '.'
	}
	return lights
}

func GetInput(filename string) Lines {
	file, _ := os.ReadFile(filename)
	inputLines := strings.Split(string(file), "\n")
	lines := make(Lines, len(inputLines))

	for i, line := range inputLines {
		elements := strings.Split(line, " ")
		line := Line{}
		lines[i] = &line

		lights := elements[0][1 : len(elements[0])-1]
		line.lights = []byte(lights)

		buttons := elements[1 : len(elements)-1]
		line.buttons = make([][]int, len(buttons))
		for j, button := range buttons {
			parsedButton := button[1 : len(button)-1]
			nums := strings.Split(parsedButton, ",")
			line.buttons[j] = make([]int, len(nums))
			for k, number := range nums {
				n, _ := strconv.Atoi(number)
				line.buttons[j][k] = n
			}
		}

		joltage := elements[len(elements)-1]
		joltageParsed := joltage[1 : len(joltage)-1]
		nums := strings.Split(joltageParsed, ",")
		line.joltage = make([]int, len(nums))
		for j, item := range nums {
			n, _ := strconv.Atoi(item)
			line.joltage[j] = n
		}
	}

	return lines
}

type Line struct {
	lights  []byte
	buttons [][]int
	joltage []int
}

func (l *Line) String() string {
	builder := strings.Builder{}

	builder.Write(l.lights)
	builder.WriteString(" ")
	for _, button := range l.buttons {
		builder.WriteString("(")
		for i, n := range button {
			builder.WriteString(strconv.Itoa(n))
			if i < len(button)-1 {
				builder.WriteString(",")
			}
		}
		builder.WriteString(") ")
	}
	builder.WriteString("{")
	for i, n := range l.joltage {
		builder.WriteString(strconv.Itoa(n))
		if i < len(l.joltage)-1 {
			builder.WriteString(",")
		}
	}
	builder.WriteString("}")

	return builder.String()
}

type Lines []*Line

func (l Lines) String() string {
	builder := strings.Builder{}
	for _, line := range l {
		builder.WriteString(fmt.Sprintln(line))
	}
	return builder.String()
}
