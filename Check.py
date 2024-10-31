import time

def get():
    with open('AllProxy.txt', 'r') as file:
        get = file.readlines()
        cleaned_lines = [line.strip() for line in get]
    return cleaned_lines

def load(num=10):
    result = []
    for count, i in enumerate(get()):
        if count >= num:
            break
        result.append(i)
    return '\n'.join(result)

# l = 0
# while True:
#     if l >= 10:
#         break
#     load(10)
#     l+=1

