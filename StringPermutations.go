package main

import (
	"fmt"
)

// permute generates all permutations of the given string using backtracking
func permute(chars []rune, left int) {
	if left == len(chars)-1 {
		fmt.Println(string(chars)) // Print the permutation
		return
	}

	// Backtracking step: swap each character to generate permutations
	for i := left; i < len(chars); i++ {
		chars[left], chars[i] = chars[i], chars[left] // Swap
		permute(chars, left+1)                        // Recurse
		chars[left], chars[i] = chars[i], chars[left] // Backtrack
	}
}

// func main() {
// 	input := "ABC"
// 	permute([]rune(input), 0)
// }
