import requests, json


def get(num=int):
    url = f'http://localhost:5000/good'

    respons = requests.get(url).json()

    # j = respons.josn().get('time')
    # print(j.get())

    return respons.get('ip') +':'+ respons.get('port')

x = get()
print(x)