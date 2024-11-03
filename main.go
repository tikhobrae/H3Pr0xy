package main

import (
	"bufio"
	"fmt"
	"net/http"
	"os"
	"regexp"
	"strings"
	"sync"
	"time"
)

// Scraper interface
type Scraper interface {
	GetURL() string
	Scrape(client *http.Client, proxies chan<- string, wg *sync.WaitGroup)
}

// BaseScraper structure
type BaseScraper struct {
	URL string
}

func (s *BaseScraper) GetURL() string {
	return s.URL
}

// GitHubScraper structure
type GitHubScraper struct {
	BaseScraper
}

func NewGitHubScraper(url string) *GitHubScraper {
	return &GitHubScraper{BaseScraper{URL: url}}
}

func (s *GitHubScraper) Scrape(client *http.Client, proxies chan<- string, wg *sync.WaitGroup) {
	defer wg.Done()

	resp, err := client.Get(s.GetURL())
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		fmt.Printf("Non-200 response: %d from %s\n", resp.StatusCode, s.GetURL())
		return
	}

	scanner := bufio.NewScanner(resp.Body)
	for scanner.Scan() {
		proxy := normalizeProxy(scanner.Text())
		if proxy != "" {
			proxies <- proxy
		}
	}

	if err := scanner.Err(); err != nil {
		fmt.Printf("Error reading response from %s: %v\n", s.GetURL(), err)
	}
}

// normalizeProxy formats a proxy to `socks5://IP:PORT`
func normalizeProxy(line string) string {
	line = strings.TrimSpace(line)
	re := regexp.MustCompile(`(\d{1,3}(?:\.\d{1,3}){3}:\d{1,5})`)
	match := re.FindString(line)
	if match != "" {
		return "socks5://" + match
	}
	return ""
}

// scrapeProxies function to scrape proxies from various sources concurrently
func scrapeProxies(output string, verbose bool) error {
	client := &http.Client{Timeout: 10 * time.Second} // Set a timeout for each request
	var wg sync.WaitGroup

	// List of GitHub sources
	scrapers := []Scraper{
		NewGitHubScraper("https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/all/data.txt"),
		NewGitHubScraper("https://raw.githubusercontent.com/zloi-user/hideip.me/main/socks5.txt"),
		NewGitHubScraper("https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt"),
		NewGitHubScraper("https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt"),
	}

	proxies := make(chan string, 5000) // Buffered channel to store proxies

	// Start scraping in parallel
	for _, scraper := range scrapers {
		wg.Add(1)
		go scraper.Scrape(client, proxies, &wg)
	}

	// Close the proxies channel when all scraping is done
	go func() {
		wg.Wait()
		close(proxies)
	}()

	// Save proxies to the output file
	file, err := os.Create(output)
	if err != nil {
		return err
	}
	defer file.Close()

	writer := bufio.NewWriter(file)
	uniqueProxies := make(map[string]struct{})
	for proxy := range proxies {
		if _, exists := uniqueProxies[proxy]; !exists {
			uniqueProxies[proxy] = struct{}{}
			writer.WriteString(proxy + "\n")
		}
	}
	return writer.Flush()
}

// Main function
func main() {
	output := "proxy/AllProxy.txt"
	verbose := true

	if err := scrapeProxies(output, verbose); err != nil {
		fmt.Println("Error:", err)
	}
	fmt.Println("Done! Proxies have been saved to", output)
}
