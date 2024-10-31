import requests, json

url = 'http://localhost:5000/time'

respons = requests.get(url)

# j = respons.josn().get('time')
# print(j.get())

print(respons.headers['content-type'], respons.text)