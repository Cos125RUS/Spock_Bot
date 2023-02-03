from os import path

def counter():
    count = 0
    while path.isfile(f'photo\{count}.jpg'):
        count += 1
    return count