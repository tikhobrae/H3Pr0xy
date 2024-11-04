from googlesearch import search

query = "free proxy list github"
urls = list(search(query, num_results=30))

for url in urls:
    print(url)