package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"io/ioutil"
	"math/rand"
	"net"
	"net/http"
	"os"
	"path/filepath"
	"strconv"
	"strings"
	"time"

	"github.com/gorilla/mux"
	"github.com/oschwald/geoip2-golang"
)

// IPInfo holds information about an IP address
type IPInfo struct {
	IP          string `json:"ip"`
	Country     string `json:"country"`
	CountryCode string `json:"country_code"`
	City        string `json:"city"`
}

// IPLookup is responsible for looking up IP information
type IPLookup struct {
	Reader *geoip2.Reader
}

// NewIPLookup initializes a new IPLookup instance
func NewIPLookup(dbPath string) (*IPLookup, error) {
	// Set default database path if not provided
	if dbPath == "" {
		dbPath = "ip_db/GeoLite2-City.mmdb"
	}

	// Check if the database file exists
	if _, err := os.Stat(dbPath); os.IsNotExist(err) {
		return nil, errors.New("database file not found at " + dbPath)
	}

	// Open the GeoIP database
	reader, err := geoip2.Open(dbPath)
	if err != nil {
		return nil, err
	}

	return &IPLookup{Reader: reader}, nil
}

// GetIPInfo retrieves information for a given IP address
func (ipl *IPLookup) GetIPInfo(ipAddress string) (IPInfo, error) {
	ip := net.ParseIP(ipAddress)
	if ip == nil {
		return IPInfo{}, errors.New("invalid IP address format")
	}

	// Lookup the IP address in the GeoIP database
	record, err := ipl.Reader.City(ip)
	if err != nil {
		return IPInfo{}, err
	}

	ipInfo := IPInfo{
		IP:          ipAddress,
		Country:     record.Country.Names["en"],
		CountryCode: record.Country.IsoCode,
		City:        record.City.Names["en"],
	}
	return ipInfo, nil
}

// Close closes the IPLookup reader
func (ipl *IPLookup) Close() {
	ipl.Reader.Close()
}

var config map[string]interface{}

func init() {
	// Load configuration from a JSON file
	configPath := filepath.Join("..", "..", "conf.json")
	loadConfig(configPath)
}

// loadConfig reads the configuration from the specified file path
func loadConfig(filePath string) {
	file, _ := os.Open(filePath)
	defer file.Close()
	data, _ := ioutil.ReadAll(file)
	json.Unmarshal(data, &config)
}

// getProxies retrieves proxies based on the specified type
func getProxies(proxyType string) []string {
	var availType string
	switch proxyType {
	case "best":
		availType = "lowping"
	case "good":
		availType = "working"
	case "all":
		availType = "allproxy"
	default:
		panic("check proxy Type!")
	}

	proxyPath := filepath.Join("..", "..", config["proxy_path"].(map[string]interface{})[availType].(string))

	file, _ := os.Open(proxyPath)
	defer file.Close()
	lines, _ := ioutil.ReadAll(file)
	return cleanLines(string(lines))
}

// cleanLines removes empty lines and whitespace from the proxy list
func cleanLines(content string) []string {
	var cleanedLines []string
	for _, line := range strings.Split(content, "\n") {
		if line = strings.TrimSpace(line); line != "" {
			cleanedLines = append(cleanedLines, line)
		}
	}
	return cleanedLines
}

// loadProxies loads a specified number of proxies and randomizes their order
func loadProxies(num int, proxyType string) []string {
	proxies := getProxies(proxyType)
	if num > len(proxies) {
		num = len(proxies)
	}
	rand.Seed(time.Now().UnixNano())
	rand.Shuffle(len(proxies), func(i, j int) {
		proxies[i], proxies[j] = proxies[j], proxies[i]
	})
	return proxies[:num]
}

// helloHandler responds with a welcome message
func helloHandler(w http.ResponseWriter, r *http.Request) {
	w.Write([]byte("Welcome, to H3Pr0xy!"))
}

// getTimeHandler responds with the current server time
func getTimeHandler(w http.ResponseWriter, r *http.Request) {
	json.NewEncoder(w).Encode(time.Now().Format(time.RFC1123))
}

// getProxyHandler retrieves a list of proxies based on the specified number
func getProxyHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")

	numStr := r.URL.Query().Get("num")
	num, err := strconv.Atoi(numStr)
	if err != nil || num <= 0 {
		num = 20 // Default number of proxies
	}

	proxies := loadProxies(num, "all")

	response := map[string]interface{}{"proxy": proxies}
	if err := json.NewEncoder(w).Encode(response); err != nil {
		http.Error(w, "Error processing JSON response", http.StatusInternalServerError)
	}
}

// getGoodHandler checks for good proxies and returns IP information
func getGoodHandler(w http.ResponseWriter, r *http.Request) {
	numStr := r.URL.Query().Get("num")
	num, err := strconv.Atoi(numStr)
	if err != nil {
		num = 3 // Default number of good proxies
	}
	proxiesList := loadProxies(num, "good")

	ipLookup, err := NewIPLookup("") // Initialize IPLookup
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer ipLookup.Close()

	for _, proxy := range proxiesList {
		client := &http.Client{
			Timeout: time.Second * 5, // Set a timeout for the request
		}

		req, err := http.NewRequest("GET", "https://httpbin.org/ip", nil)
		if err != nil {
			continue
		}

		// Set the proxy for the request
		req.Header.Set("Proxy", "socks5://"+proxy)
		resp, err := client.Do(req)
		if err != nil {
			continue
		}
		defer resp.Body.Close()

		// If the response is OK, retrieve the IP information
		if resp.StatusCode == http.StatusOK {
			ipInfo, _ := ipLookup.GetIPInfo(proxy)

			json.NewEncoder(w).Encode(map[string]interface{}{
				"ip":      ipInfo.IP,
				"country": ipInfo.Country,
				"cc":      ipInfo.CountryCode,
				"port":    proxy,
			})
			return
		}
	}
	http.Error(w, "No valid proxy available", http.StatusInternalServerError)
}

func main() {
	// Set up the router and define the routes
	router := mux.NewRouter()
	router.HandleFunc("/", helloHandler).Methods("GET")
	router.HandleFunc("/time", getTimeHandler).Methods("GET")
	router.HandleFunc("/getproxy", getProxyHandler).Methods("GET")
	router.HandleFunc("/good", getGoodHandler).Methods("GET")

	// Start the HTTP server
	http.ListenAndServe(":8080", router)
	fmt.Println("Run API on: 8080")
}
