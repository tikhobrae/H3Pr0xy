import requests, time

pnum = 40
path = "src/GO/GoScanner/cmd/mubeng/proxy.txt"
allrun = 0
n = 0

while True:
    url = f"http://localhost:8080/getproxy?num={pnum}"

    response = requests.get(url)

    x = response.json()
    all = x.get('proxy')
    allrun +=1
    print('-'*10, allrun, '-'*10, sep='|')
    with open(path, "w") as file:
        for i in all:
            file.write(i + '\n')
            n+=1
        print(f"get '{n}' proxies. save here '{path}'")
    n = 0
    time.sleep(20)