# # import کردن کلاس IPLookup از ماژول ip_lookup
# from ip_lookup import IPLookup

# # ایجاد نمونه‌ای از کلاس و تعیین مسیر دیتابیس
# ip_lookup = IPLookup()

# # دریافت اطلاعات مربوط به IP
# ip_address = "8.8.8.8"
# ip_info = ip_lookup.get_ip_info(ip_address)
# print(ip_info)

# # بستن کانکشن دیتابیس پس از پایان کار
# ip_lookup.close()

import requests, time
import load, os

def remove(file_name=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'proxy', 'working.txt'), which=str):
    with open(file_name, "r") as file:
        lines = file.readlines()

    # داده خاص را از خطوط حذف کنید
    # در اینجا فرض می‌کنیم می‌خواهیم تمامی خطوطی که شامل کلمه "test" هستند حذف شوند
    new_lines = [line for line in lines if which not in line]

    # نوشتن محتوای جدید بدون داده‌های حذف شده به فایل
    with open(file_name, "w") as file:
        file.writelines(new_lines)

def test():
    proxies_list = load.load(10, type='good')
    for proxy in proxies_list:
        proxies = {
            'http': f'socks5://{proxy}',
            'https': f'socks5://{proxy}'
        }
        try:
            response = requests.get('https://httpbin.org/ip', proxies=proxies, timeout=8)
            response.raise_for_status() 
            print({'ok' : response.status_code}, proxy)
        except requests.RequestException:
            remove(which=proxy)
            print({'not work this': proxy})
            continue

test()