import requests, json


def get(num=int):
    url = f'http://localhost:5000/good'

    respons = requests.get(url)

    # j = respons.josn().get('time')
    # print(j.get())
    if respons.status_code == 200:
        return respons.json().get('ip') +':'+ respons.json().get('port')
    else:
        return respons.status_code, ' : ', respons.json().get('error')

x = get()
print(x)