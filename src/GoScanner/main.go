package main

import (
	"encoding/json"
	"errors"
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

// ساختار برای اطلاعات IP
type IPInfo struct {
	IP          string `json:"ip"`
	Country     string `json:"country"`
	CountryCode string `json:"country_code"`
	City        string `json:"city"`
}

// ساختار برای مدیریت اطلاعات IP
type IPLookup struct {
	Reader *geoip2.Reader
}

// تابع برای ایجاد یک نمونه جدید از IPLookup
func NewIPLookup(dbPath string) (*IPLookup, error) {
	if dbPath == "" {
		dbPath = "ip_db/GeoLite2-City.mmdb" // مسیر پیش‌فرض به پایگاه داده
	}

	if _, err := os.Stat(dbPath); os.IsNotExist(err) {
		return nil, errors.New("database file not found at " + dbPath)
	}

	reader, err := geoip2.Open(dbPath)
	if err != nil {
		return nil, err
	}

	return &IPLookup{Reader: reader}, nil
}

// تابع برای دریافت اطلاعات IP
func (ipl *IPLookup) GetIPInfo(ipAddress string) (IPInfo, error) {
	ip := net.ParseIP(ipAddress) // تبدیل string به net.IP
	if ip == nil {
		return IPInfo{}, errors.New("invalid IP address format")
	}

	record, err := ipl.Reader.City(ip) // استفاده از net.IP
	if err != nil {
		return IPInfo{}, err // در اینجا می‌توانید خطا را مدیریت کنید
	}

	ipInfo := IPInfo{
		IP:          ipAddress,
		Country:     record.Country.Names["en"],
		CountryCode: record.Country.IsoCode,
		City:        record.City.Names["en"],
	}
	return ipInfo, nil
}

func (ipl *IPLookup) Close() {
	ipl.Reader.Close()
}

// بارگذاری پروکسی‌ها
var config map[string]interface{}

func init() {
	configPath := filepath.Join("..", "..", "conf.json")
	loadConfig(configPath)
}

func loadConfig(filePath string) {
	file, _ := os.Open(filePath)
	defer file.Close()
	data, _ := ioutil.ReadAll(file)
	json.Unmarshal(data, &config)
}

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

func cleanLines(content string) []string {
	var cleanedLines []string
	for _, line := range strings.Split(content, "\n") {
		if line = strings.TrimSpace(line); line != "" {
			cleanedLines = append(cleanedLines, line)
		}
	}
	return cleanedLines
}

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

func helloHandler(w http.ResponseWriter, r *http.Request) {
	w.Write([]byte("Welcome, to H3Pr0xy!"))
}

func getTimeHandler(w http.ResponseWriter, r *http.Request) {
	json.NewEncoder(w).Encode(time.Now().Format(time.RFC1123))
}

func getProxyHandler(w http.ResponseWriter, r *http.Request) {
	// تنظیم نوع پاسخ به JSON
	w.Header().Set("Content-Type", "application/json")

	// دریافت پارامتر num از درخواست و تبدیل به عدد
	numStr := r.URL.Query().Get("num")
	num, err := strconv.Atoi(numStr)
	if err != nil || num <= 0 { // بررسی مقدار نامعتبر
		num = 20 // مقدار پیش‌فرض
	}

	// بارگذاری پروکسی‌ها
	proxies := loadProxies(num, "all")

	// بازگردانی نتیجه به صورت JSON
	response := map[string]interface{}{"proxy": proxies}
	if err := json.NewEncoder(w).Encode(response); err != nil {
		http.Error(w, "خطا در پردازش پاسخ JSON", http.StatusInternalServerError)
	}
}

func getGoodHandler(w http.ResponseWriter, r *http.Request) {
	numStr := r.URL.Query().Get("num")
	num, err := strconv.Atoi(numStr) // تبدیل num به int
	if err != nil {
		num = 3 // مقدار پیش‌فرض در صورت بروز خطا
	}
	proxiesList := loadProxies(num, "good") // بارگذاری پروکسی‌های خوب

	ipLookup, err := NewIPLookup("") // در اینجا می‌توانید مسیر پایگاه داده خود را وارد کنید
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer ipLookup.Close()

	for _, proxy := range proxiesList {
		client := &http.Client{
			Timeout: time.Second * 5,
		}

		req, err := http.NewRequest("GET", "https://httpbin.org/ip", nil)
		if err != nil {
			continue
		}

		req.Header.Set("Proxy", "socks5://"+proxy) // تنظیم پروکسی
		resp, err := client.Do(req)
		if err != nil {
			continue // بارگذاری پروکسی نامعتبر
		}
		defer resp.Body.Close()

		if resp.StatusCode == http.StatusOK {
			ipInfo, _ := ipLookup.GetIPInfo(proxy) // دریافت اطلاعات IP

			json.NewEncoder(w).Encode(map[string]interface{}{
				"ip":      ipInfo.IP,
				"country": ipInfo.Country,
				"cc":      ipInfo.CountryCode,
				"port":    proxy, // یا اگر بخواهید فقط پورت را دریافت کنید
			})
			return
		}
	}
	http.Error(w, "No valid proxy available", http.StatusInternalServerError)
}

func main() {
	router := mux.NewRouter()
	router.HandleFunc("/", helloHandler).Methods("GET")
	router.HandleFunc("/time", getTimeHandler).Methods("GET")
	router.HandleFunc("/getproxy", getProxyHandler).Methods("GET")
	router.HandleFunc("/good", getGoodHandler).Methods("GET")

	http.ListenAndServe(":8080", router)
}
