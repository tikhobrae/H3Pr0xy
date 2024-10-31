import requests

link = "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt"
f = requests.get(link)
# print(f.text)

# with open('AllProxy.txt', 'w') as file:
#     file.write(f.text)

for i in f.text:
        print(i)