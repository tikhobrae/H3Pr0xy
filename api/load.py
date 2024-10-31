import json
import os
import random
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'conf.json')

def load_config(file_path=config_path) -> json:
    with open(file_path, 'r') as conf:
        config = json.load(conf)
    return config

config = load_config()

def get(proxy_type=str) -> list:

    if proxy_type == 'best':
        avail_type = 'lowping'
    elif proxy_type == 'good':
        avail_type = 'working'
    elif proxy_type == 'all':
        avail_type = 'allproxy'
    else:
        raise ValueError('check proxy Type!')

    proxy_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', config['proxy_path'][avail_type])
    
    with open(proxy_path, 'r') as file:
        get = file.readlines()
        cleaned_lines = [line.strip() for line in get if line.strip()] 
    return cleaned_lines

# def load(num, type=str) -> list:
#     result = []
#     for count, proxy in enumerate(get(proxy_type=type)):
#         if count >= num:
#             break
#         result.append(proxy)  
#     return result  

def load(num, type=str) -> list:
    proxies = get(proxy_type=type)
    
    if num > len(proxies):
        num = len(proxies)  
    
    result = random.sample(proxies, num)
    return result

def remove(proxy_type=str, which=str) -> None:

    if proxy_type == 'best':
        avail_type = 'lowping'
    elif proxy_type == 'good':
        avail_type = 'working'
    elif proxy_type == 'all':
        avail_type = 'allproxy'
    else:
        raise ValueError('check proxy Type!')

    proxy_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', config['proxy_path'][avail_type])
    
    with open(proxy_path, "r") as file:
        lines = file.readlines()
    new_lines = [line for line in lines if which not in line]
    with open(proxy_path, "w") as file:
        file.writelines(new_lines)