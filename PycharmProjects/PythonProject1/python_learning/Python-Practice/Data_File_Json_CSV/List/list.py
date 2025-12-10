numbers = [1,2,3,4]
'''
new_list = []
for n in numbers:
    new_item = n+1
    new_list.append(new_item)

print(new_list)
'''

new_list = [n+1 for n in numbers]
print(new_list)

name = "saiteja"
new_name = [letter for letter in name]
print(new_name)

names = ['sai', 'teja', 'himaja', 'himu']

names_to_remove = [name for name in names if len(name)<5]
print(names_to_remove)