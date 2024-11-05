import requests
import re
import base64
import random
from transformers import pipeline

GITHUB_TOKEN = 'GitHub Api Key'  # Insert your token here
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# List of different search queries to change the search term automatically
search_queries = [
    "socks5 list",
    "free proxy list",
    # "public proxy repository",
    # "proxy server list",
    # "http proxies",
    # "socks4 proxies",
    # "proxy collection"
]

# Natural language processing model
nlp_model = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

# Search GitHub repositories
def search_github_repositories(query):
    url = "https://api.github.com/search/repositories"
    params = {"q": query, "sort": "stars", "order": "desc", "per_page": 10}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()["items"]

# Retrieve files from the repository
def get_repository_files(repo_full_name):
    url = f"https://api.github.com/repos/{repo_full_name}/contents"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# Download README file content
def download_readme(repo_full_name):
    readme_url = f"https://api.github.com/repos/{repo_full_name}/readme"
    response = requests.get(readme_url, headers=headers)
    response.raise_for_status()
    return response.json()['content']

# Download proxy file content
def download_proxy_file(url):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

# Extract proxies with regular expressions
def extract_proxies(data):
    return re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{2,5}\b', data)

# Classify proxy type
def classify_proxies(proxies, filename):
    proxy_dict = {
        "socks5": [],
        "socks4": [],
        "http": [],
        "https": []
    }
    
    for proxy in proxies:
        if "socks5" in filename.lower():
            proxy_dict["socks5"].append(proxy)
        elif "socks4" in filename.lower():
            proxy_dict["socks4"].append(proxy)
        elif "http" in filename.lower() or "https" in filename.lower():
            proxy_dict["http"].append(proxy)
        else:
            print(f"Unknown proxy format in {filename}: {proxy}")

    return proxy_dict

# Main process execution
if __name__ == "__main__":
    # Select a random search query from the list
    selected_query = random.choice(search_queries)
    print(f"Selected search query: {selected_query}")
    
    repos = search_github_repositories(selected_query)
    
    all_proxy_dict = {
        "socks5": [],
        "socks4": [],
        "http": [],
        "https": []
    }

    for repo in repos:
        print(f"Searching in repository: {repo['html_url']}")
        
        try:
            # Download README
            readme_content = download_readme(repo["full_name"])
            readme_text = base64.b64decode(readme_content).decode('utf-8')

            # Extract proxy file names from README
            proxy_file_names = re.findall(r'\b(?:socks5|socks4|http|https)[\w\-]*\.?(txt|json)\b', readme_text, re.IGNORECASE)
            print(f"Proxy file names mentioned in README: {proxy_file_names}")

            # Retrieve files from repository
            files = get_repository_files(repo["full_name"])
            found_files = []

            # Search in file names
            for file in files:
                if file["type"] == "file":
                    # Check file names
                    if file["name"].lower() in proxy_file_names:
                        found_files.append(file["name"])
                    else:
                        # Check standard names
                        standard_names = ["socks5.txt", "socks4.txt", "http.txt", "https.txt", "proxy.txt", "data.txt"]
                        if file["name"].lower() in standard_names:
                            found_files.append(file["name"])

            # Download found proxy files
            for found_file in found_files:
                print(f"Found proxy file: {found_file} in {repo['html_url']}")
                proxy_data = download_proxy_file(file["download_url"])
                
                proxies = extract_proxies(proxy_data)
                proxy_dict = classify_proxies(proxies, found_file)
                
                # Merge proxies into main dictionary
                for proxy_type in all_proxy_dict.keys():
                    all_proxy_dict[proxy_type].extend(proxy_dict[proxy_type])
                            
        except Exception as e:
            print(f"Error processing repository {repo['html_url']}: {e}")

    # Save proxies to respective files
    for proxy_type, proxies in all_proxy_dict.items():
        if proxies:
            with open(f"{proxy_type}.txt", "w", encoding="utf-8") as f:
                for proxy in proxies:
                    f.write(f"{proxy_type}://{proxy}" + "\n")
            print(f"> Saved {len(proxies)} {proxy_type} proxies to {proxy_type}.txt")
        else:
            print(f"No proxies found for {proxy_type}")

    print("All proxies collected and saved to their respective files.")
