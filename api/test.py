# import کردن کلاس IPLookup از ماژول ip_lookup
from ip_lookup import IPLookup

# ایجاد نمونه‌ای از کلاس و تعیین مسیر دیتابیس
ip_lookup = IPLookup()

# دریافت اطلاعات مربوط به IP
ip_address = "8.8.8.8"
ip_info = ip_lookup.get_ip_info(ip_address)
print(ip_info)

# بستن کانکشن دیتابیس پس از پایان کار
ip_lookup.close()
