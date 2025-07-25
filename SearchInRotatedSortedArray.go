package main

import "fmt"

// binarySearch performs iterative binary search
func binarySearch(arr []int, target int) int {
	left, right := 0, len(arr)-1

	for left <= right {
		mid := left + (right-left)/2 // Avoids potential overflow

		if arr[mid] == target {
			return mid // Target found, return index
		} else if arr[mid] < target {
			left = mid + 1 // Search in the right half
		} else {
			right = mid - 1 // Search in the left half
		}
	}

	return -1 // Target not found
}

// search_recur recursively searches for the target
func search_recur(nums []int, target int) (int, bool) {
	if len(nums) <= 0 {
		return -1, false
	}
	if len(nums) == 1 {
		if target == nums[0] {
			return 0, true
		}
		return -1, false
	}

	// If the array is rotated (first element is greater than the last)
	if nums[0] > nums[len(nums)-1] {
		mid := len(nums) / 2

		leftIndex, leftFound := search_recur(nums[:mid], target)
		if leftFound {
			return leftIndex, true
		}

		rightIndex, rightFound := search_recur(nums[mid:], target)
		if rightFound {
			return mid + rightIndex, true // Adjust for offset
		}

		return -1, false
	}

	// If array is sorted normally, use binary search
	index := binarySearch(nums, target)
	if index != -1 {
		return index, true
	}
	return -1, false
}
func search(nums []int, target int) int {

	temp := -1
	if len(nums) <= 0 {
		return temp
	}
	if len(nums) == 1 {

		if target == nums[0] {
			temp = 0
		}
		return temp
	}
	val, _ := search_recur(nums, target)
	return val

}

func main() {

	fmt.Println(search([]int{4, 5, 6, 7, 0, 1, 2}, 0))
}
