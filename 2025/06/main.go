package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	file, _ := os.ReadFile("in.txt")
	input := GetInput(file)

	sol := sol2(input)

	fmt.Println(sol)
}

func sol1(input *Input) int {
	sol := 0

	for x, operator := range input.operators {
		columnResult := 0

		for _, line := range input.nums {
			switch operator {
			case "+":
				columnResult += line[x]
			case "*":
				if columnResult == 0 {
					columnResult = 1
				}
				columnResult *= line[x]
			}
		}

		sol += columnResult
	}

	return sol
}

func sol2(input *Input) int {
	sol := 0

	for x, operator := range input.operators {
		columnResult := 0
		if operator == "*" {
			columnResult = 1
		}

		for xx := range input.sNums[0][x] {
			currentLineNumber := strings.Builder{}

			for _, line := range input.sNums {
				sNumber := line[x]
				digit := sNumber[xx]
				if string(digit) != " " {
					currentLineNumber.WriteByte(digit)
				}
			}

			n, _ := strconv.Atoi(currentLineNumber.String())

			switch operator {
			case "+":
				columnResult += n
			case "*":
				columnResult *= n
			}
		}

		// fmt.Println(columnResult)
		sol += columnResult
	}

	return sol
}

func GetInput(file []byte) *Input {
	lines := strings.Split(string(file), "\n")
	width := len(strings.Fields(lines[0]))

	nums := make([][]int, len(lines)-1)

	operatorsLine := lines[len(lines)-1]
	operators := strings.Fields(operatorsLine)

	for i, line := range lines[:len(lines)-1] {
		nums[i] = make([]int, width)
		fields := strings.Fields(line)
		for j, field := range fields {
			n, _ := strconv.Atoi(field)
			nums[i][j] = n
		}
	}

	return &Input{
		nums:      nums,
		sNums:     parseSNumbers(lines),
		operators: operators,
	}
}

func parseSNumbers(lines []string) [][]string {
	numberOfColumns := len(strings.Fields(lines[0]))

	maxNumberLenByColumn := make([]int, numberOfColumns)

	for _, line := range lines[:len(lines)-1] {
		lineSNumbers := strings.Fields(line)
		for colIndex, sNum := range lineSNumbers {
			if maxNumberLenByColumn[colIndex] < len(sNum) {
				maxNumberLenByColumn[colIndex] = len(sNum)
			}
		}
	}

	sNumbers := make([][]string, len(lines)-1)

	for lineIndex, line := range lines[:len(lines)-1] {
		row := make([]string, numberOfColumns)
		numberCount := 0

		for i := 0; i < len(line); i++ {
			sNumber := line[i : i+maxNumberLenByColumn[numberCount]]
			row[numberCount] = sNumber
			i += maxNumberLenByColumn[numberCount]
			numberCount++
			if numberCount == numberOfColumns {
				break
			}
		}

		sNumbers[lineIndex] = row
	}

	return sNumbers
}

type Input struct {
	nums      [][]int
	sNums     [][]string
	operators []string
}
