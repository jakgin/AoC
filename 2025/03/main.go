package main

import (
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
)

func main() {
	var sol int64
	file, _ := os.ReadFile("in.txt")
	lines := strings.SplitSeq(string(file), "\n")

	for line := range lines {
		sol += joltage(line, 12)
	}

	fmt.Println(sol)
}

func joltage(line string, n int) int64 {
	numbers := stringSliceToInts(line)
	maxNums := make([]int, n)

	maxIndex := -1

	for i := range n {
		localMaxNumber := 0
		for j := maxIndex + 1; j <= len(numbers)-n+i; j++ {
			if numbers[j] > localMaxNumber {
				localMaxNumber = numbers[j]
				maxIndex = j
			}
		}
		maxNums[i] = localMaxNumber
	}

	return concatenateNumber(maxNums)
}

func stringSliceToInts(s string) []int {
	numbers := make([]int, len(s))
	for i := 0; i < len(s); i++ {
		n, _ := strconv.Atoi(string(s[i]))
		numbers[i] = n
	}
	return numbers
}

func concatenateNumber(nums []int) int64 {
	var result int64

	for i := range len(nums) {
		result += int64(math.Pow10(i)) * int64(nums[len(nums)-i-1])
	}

	return result
}
