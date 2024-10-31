import json
import os

config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'conf.json')

def load_config(file_path=config_path):
    with open(file_path, 'r') as conf:
        config = json.load(conf)
    return config

config = load_config()

def get(proxy_type=str) -> list:
    proxy_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', config['proxy_path'][proxy_type])
    
    with open(proxy_path, 'r') as file:
        get = file.readlines()
        cleaned_lines = [line.strip() for line in get if line.strip()]  # حذف خطوط خالی و کاراکترهای اضافی
    return cleaned_lines

def load(num) -> list:
    result = []
    for count, proxy in enumerate(get()):
        if count >= num:
            break
        result.append(proxy)  
    return result  

