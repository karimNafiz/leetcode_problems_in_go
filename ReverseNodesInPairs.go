package main

import "fmt"

// Definition for singly-linked list.
type ListNode struct {
	Val  int
	Next *ListNode
}

// Main function that starts swapping pairs
func swapPairs(head *ListNode) *ListNode {
	length := GetLength(head)
	if length < 2 {
		return head
	}
	return swapPairsRecursive(head, length)
}

// Recursive function to swap nodes in pairs
func swapPairsRecursive(head *ListNode, remLen int) *ListNode {
	if remLen < 2 {
		return head
	}

	// Swap nodes
	tempNext := swapPairsRecursive(head.Next.Next, remLen-2)
	tempHead := head.Next
	head.Next = tempNext
	tempHead.Next = head

	return tempHead
}

// Function to get the length of the linked list
func GetLength(head *ListNode) int {
	temp := head
	length := 0
	for temp != nil {
		length++
		temp = temp.Next
	}
	return length
}

// Helper function to create a linked list from a slice
func createList(vals []int) *ListNode {
	if len(vals) == 0 {
		return nil
	}
	head := &ListNode{Val: vals[0]}
	curr := head
	for _, v := range vals[1:] {
		curr.Next = &ListNode{Val: v}
		curr = curr.Next
	}
	return head
}

// Helper function to print the linked list
func printList(head *ListNode) {
	curr := head
	for curr != nil {
		fmt.Print(curr.Val, " -> ")
		curr = curr.Next
	}
	fmt.Println("nil")
}

// Test the function
func main() {
	head := createList([]int{1, 2, 3, 4})
	fmt.Println("Original list:")
	printList(head)

	newHead := swapPairs(head)
	fmt.Println("After swapping pairs:")
	printList(newHead)
}
