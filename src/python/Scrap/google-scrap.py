import requests
from googlesearch import search
import re
from transformers import pipeline
from bs4 import BeautifulSoup

# NLP Model
nlp = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

# Google Search
def google_search(query, num_results=30):
    return list(search(query, num_results=num_results))

# Fetch Content
def fetch_content(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

# Proxy Content Check
def is_proxy_content(text):
    result = nlp(text[:1000])  
    return "proxy" in result[0]["label"].lower() 

# Extract Proxies
def extract_proxies(text):
    return re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{2,5}\b', text)

# Main Execution
if __name__ == "__main__":
    query = "free proxy list github"
    urls = google_search(query)

    proxies = []

    for url in urls:
        print(f"Fetching: {url}")
        content = fetch_content(url)
        
        # Parse Text
        soup = BeautifulSoup(content, "html.parser")
        text = soup.get_text(separator=" ")

        # Check & Extract Proxies
        if is_proxy_content(text):
            found_proxies = extract_proxies(text)
            proxies.extend(found_proxies)
            print(f"Found {len(found_proxies)} proxies in {url}")

    # Save Proxies
    with open("proxies.txt", "w") as f:
        for proxy in set(proxies):  # Remove Duplicates
            f.write(proxy + "\n")
    print(f"Total proxies saved: {len(set(proxies))}")
