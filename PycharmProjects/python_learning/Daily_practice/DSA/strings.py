def diff_of_names(name1,name2):
    return set(name1)-set(name2), set(name2)-set(name1)




name1 = 'abcd'
name2 = 'abcde'

print(diff_of_names(name1,name2))