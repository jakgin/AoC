package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	sol := 0
	file, _ := os.ReadFile("in.txt")
	ranges := strings.SplitSeq(string(file), ",")

	for r := range ranges {
		rng := getRange(r)
		sol += getInvalidIndexesSumFromRange(rng)
	}

	fmt.Println("Sum of invalid indexes:", sol)
}

func getRange(rng string) Rng {
	elements := strings.Split(rng, "-")
	first, _ := strconv.Atoi(elements[0])
	last, _ := strconv.Atoi(elements[1])
	return Rng{first, last}
}

func getInvalidIndexesSumFromRange(rng Rng) int {
	sum := 0
	for n := rng.first; n <= rng.last; n++ {
		if isInvalid2(n) {
			sum += n
		}
	}
	return sum
}

func isInvalid(n int) bool {
	s := strconv.Itoa(n)

	if len(s)%2 != 0 {
		return false
	}

	a := s[:len(s)/2]
	b := s[len(s)/2:]

	return a == b
}

func isInvalid2(n int) bool {
	s := strconv.Itoa(n)

	for i := 1; i < len(s); i++ {
		if len(s)%i != 0 {
			continue
		}

		pattern := s[:i]
		pass := true
		for j := i; j < len(s); j += i {
			if s[j:j+i] != pattern {
				pass = false
				break
			}
		}

		if pass {
			return true
		}
	}

	return false
}

type Rng struct {
	first int
	last  int
}
