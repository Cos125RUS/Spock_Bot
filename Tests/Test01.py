from os import *

i = 0
while path.isfile(f'{i}.jpg'):
    i+=1

print(i)

