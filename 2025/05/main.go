package main

import (
	"cmp"
	"fmt"
	"os"
	"slices"
	"strconv"
	"strings"
)

func main() {
	file, _ := os.ReadFile("in.txt")
	var ranges []Range = GetRanges(file)
	var numbers []int64 = GetNumbers(file)

	sol := sol2(ranges, numbers)

	fmt.Println(sol)
}

func sol2(ranges []Range, numbers []int64) int64 {
	var sol int64

	combinedRanges := CombineRanges(ranges)

	for _, r := range combinedRanges {
		sol += r.max - r.min + 1
	}

	return sol
}

func sol1(ranges []Range, numbers []int64) int64 {
	var sol int64

	for _, n := range numbers {
		for _, r := range ranges {
			if r.isInRange(n) {
				sol++
				break
			}
		}
	}

	return sol
}

func CombineRanges(ranges []Range) []Range {
	slices.SortFunc(ranges, func(a Range, b Range) int {
		return cmp.Compare(a.min, b.min)
	})

	combinedRanges := []Range{}
	for i := 0; i < len(ranges)-1; i++ {
		if ranges[i].isInRange(ranges[i+1].min) {
			ranges[i+1].min = ranges[i].min
			if ranges[i].max > ranges[i+1].max {
				ranges[i+1].max = ranges[i].max
			}
		} else {
			combinedRanges = append(combinedRanges, ranges[i])
		}
	}
	combinedRanges = append(combinedRanges, ranges[len(ranges)-1])
	return combinedRanges
}

func GetRanges(file []byte) []Range {
	input := strings.Split(string(file), "\n\n")
	lines := strings.Split(input[0], "\n")
	ranges := make([]Range, len(lines))
	for i, line := range lines {
		items := strings.Split(line, "-")
		min, _ := strconv.ParseInt(items[0], 10, 0)
		max, _ := strconv.ParseInt(items[1], 10, 0)
		ranges[i] = Range{min, max}
	}

	return ranges
}

func GetNumbers(file []byte) []int64 {
	input := strings.Split(string(file), "\n\n")
	lines := strings.Split(input[1], "\n")
	nums := make([]int64, len(lines))
	for i, line := range lines {
		n, _ := strconv.ParseInt(line, 10, 0)
		nums[i] = n
	}
	return nums
}

type Range struct {
	min, max int64
}

func (r *Range) isInRange(n int64) bool {
	return n >= r.min && n <= r.max
}
