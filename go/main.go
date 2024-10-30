package main

import (
	"bufio"
	"fmt"
	"net/http"
	"os"
	"sync"
	"time"

	"golang.org/x/net/proxy"
)

func checkProxy(proxyAddress string, wg *sync.WaitGroup, workingProxies chan<- string) {
	defer wg.Done()

	dialer, err := proxy.SOCKS5("tcp", proxyAddress, nil, proxy.Direct)
	if err != nil {
		fmt.Printf("Failed to create dialer for proxy %s: %v\n", proxyAddress, err)
		return
	}

	httpTransport := &http.Transport{
		Dial: dialer.Dial,
	}
	client := &http.Client{
		Transport: httpTransport,
		Timeout:   30 * time.Second,
	}

	resp, err := client.Get("https://httpbin.org/ip")
	if err != nil {
		fmt.Printf("Request failed for proxy %s: %v\n", proxyAddress, err)
		return
	}
	defer resp.Body.Close()

	if resp.StatusCode == http.StatusOK {
		fmt.Printf("Proxy %s is working\n", proxyAddress)
		workingProxies <- proxyAddress
	} else {
		fmt.Printf("Proxy %s returned status code: %d\n", proxyAddress, resp.StatusCode)
	}
}

func main() {
	file, err := os.Open("text.txt")
	if err != nil {
		fmt.Println("Error opening file:", err)
		return
	}
	defer file.Close()

	outputFile, err := os.Create("working_proxies.txt")
	if err != nil {
		fmt.Println("Error creating output file:", err)
		return
	}
	defer outputFile.Close()

	scanner := bufio.NewScanner(file)
	var wg sync.WaitGroup
	workingProxies := make(chan string)

	go func() {
		for proxyAddress := range workingProxies {
			_, err := outputFile.WriteString(proxyAddress + "\n")
			if err != nil {
				fmt.Println("Error writing to output file:", err)
			}
		}
	}()

	for scanner.Scan() {
		proxyAddress := scanner.Text()
		wg.Add(1)
		go checkProxy(proxyAddress, &wg, workingProxies)
	}

	if err := scanner.Err(); err != nil {
		fmt.Println("Error reading file:", err)
	}

	wg.Wait()
	close(workingProxies)

	fmt.Println("Proxy check complete. Check 'working_proxies.txt' for valid proxies.")
}
