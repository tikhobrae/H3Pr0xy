import requests

link = "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt"
f = requests.get(link)
print(f.text)

with open('AllProxy.txt', 'w') as file:
    file.write(f.text)
# import urllib.request

# link = "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt"
# f = urllib.request.urlopen(link)
# myfile = f.readline()
# print(myfile)