package main

import (
	"bufio"
	"fmt"
	"net/http"
	"os"
)

func main() {
	// The URL containing the SOCKS5 proxy list
	url := "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt"

	// Create or open the output file
	filename := "text.txt"
	file, err := os.Create(filename)
	if err != nil {
		fmt.Println("Error creating file:", err)
		return
	}
	defer file.Close()

	// Send HTTP GET request
	res, err := http.Get(url)
	if err != nil {
		fmt.Println("Error fetching URL:", err)
		return
	}
	defer res.Body.Close()

	// Check for HTTP response status
	if res.StatusCode != http.StatusOK {
		fmt.Println("Error: status code", res.StatusCode)
		return
	}

	// Use a scanner to read the response body line by line
	scanner := bufio.NewScanner(res.Body)
	fmt.Println("save SOCKS5 Proxy in : ", filename)
	for scanner.Scan() {
		proxy := scanner.Text() // Read each line (proxy address)
		// fmt.Println(proxy)      // Print to the terminal

		// Write the proxy address to the file, appending a newline
		if _, err := file.WriteString(proxy + "\n"); err != nil {
			fmt.Println("Error writing to file:", err)
			return
		}
	}

	// Check for errors during scanning
	if err := scanner.Err(); err != nil {
		fmt.Println("Error reading response body:", err)
	}
}
