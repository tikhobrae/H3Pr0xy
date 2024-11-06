import requests
import re
import base64
import random
import logging
from concurrent.futures import ThreadPoolExecutor
from transformers import pipeline

# Initialize constants and NLP model
GITHUB_TOKEN = 'GitHub Api Key'
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}
search_queries = [f"{type} proxy list" for type in ["socks5", "socks4", "http", "https"]]
nlp_model = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

# Set up logging
logging.basicConfig(filename='proxy_collector.log', level=logging.INFO)

# Search GitHub repositories
def search_github_repositories(query):
    url = "https://api.github.com/search/repositories"
    params = {"q": query, "sort": "stars", "order": "desc", "per_page": 10}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()["items"]

# Retrieve files from the repository
def get_repository_files(repo_full_name, path=""):
    url = f"https://api.github.com/repos/{repo_full_name}/contents/{path}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# Download and decode file content
def download_file_content(url):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return base64.b64decode(response.json()['content']).decode('utf-8')

# Extract proxies with regular expressions
def extract_proxies(data):
    # Refined regex pattern to match IP:PORT
    pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}:\d{2,5}\b'
    return re.findall(pattern, data)

# Classify proxy type based on filename
def classify_proxies(proxies, filename):
    proxy_dict = {
        "socks5": set(),
        "socks4": set(),
        "http": set(),
        "https": set()
    }
    
    # Classify based on filename patterns
    if "socks5" in filename.lower():
        proxy_dict["socks5"].update(proxies)
    elif "socks4" in filename.lower():
        proxy_dict["socks4"].update(proxies)
    elif "http" in filename.lower() or "https" in filename.lower():
        proxy_dict["http"].update(proxies)
    else:
        print(f"Unknown proxy format in {filename}: {proxies}")

    return proxy_dict

# Save proxies to files
def save_proxies_to_file(proxy_dict):
    for proxy_type, proxies in proxy_dict.items():
        if proxies:
            file_path = f"{proxy_type}.txt"
            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines([f"{proxy_type}://{proxy}\n" for proxy in proxies])
            print(f"> Saved {len(proxies)} unique {proxy_type} proxies to {file_path}")

# Main process execution
if __name__ == "__main__":
    # Select a random search query from the list
    selected_query = random.choice(search_queries)
    print(f"Selected search query: {selected_query}")
    
    # Execute search
    repos = search_github_repositories(selected_query)
    
    # Master dictionary to store unique proxies
    all_proxy_dict = {
        "socks5": set(),
        "socks4": set(),
        "http": set(),
        "https": set()
    }

    for repo in repos:
        print(f"Searching in repository: {repo['html_url']}")
        
        try:
            # Get files from repository root
            files = get_repository_files(repo["full_name"])
            proxy_files = []

            # Identify possible proxy files by keywords in filenames
            for file in files:
                if file["type"] == "file" and re.search(r'(socks5|socks4|http|https|proxy)\.(txt|json)', file["name"], re.IGNORECASE):
                    proxy_files.append(file)

            # Process each identified proxy file
            for proxy_file in proxy_files:
                print(f"Found proxy file: {proxy_file['name']} in {repo['html_url']}")
                file_content = download_file_content(proxy_file["download_url"])
                
                # Extract proxies
                proxies = extract_proxies(file_content)
                
                # Classify proxies and update main dictionary
                proxy_dict = classify_proxies(proxies, proxy_file["name"])
                for proxy_type, proxy_set in proxy_dict.items():
                    all_proxy_dict[proxy_type].update(proxy_set)
                    
        except Exception as e:
            logging.error(f"Error processing repository {repo['html_url']}: {e}")

    # Save unique proxies to respective files
    save_proxies_to_file(all_proxy_dict)
    print("All unique proxies collected and saved to their respective files.")
