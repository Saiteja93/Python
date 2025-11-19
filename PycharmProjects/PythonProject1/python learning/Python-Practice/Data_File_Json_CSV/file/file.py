import os
print(os.getcwd())

with open("../practice/file/text.txt") as f:
    file = f.read()
    print(file)
