package main

import (
	"fmt"
	"net/http"
)

// Handler is a function type for HTTP requests
type Handler func(http.ResponseWriter, *http.Request)

func main() {
	// Testing slices, maps and goroutines
	m := map[string]int{"apple": 5, "banana": 10}
	fmt.Printf("Apple count: %d\n", m["apple"])

	go func() {
		fmt.Println("Running in background")
	}()
}
