def get():
    with open('AllProxy.txt', 'r') as file:
        get = file.readlines()
        cleaned_lines = [line.strip() for line in get]
    return cleaned_lines

for i in get():
    print(i)