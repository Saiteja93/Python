

def word_finder(name):
    words = {}
    for s in name:
        if s in words:
            words[s]+=1
        else:
            words[s]=1
    return words


name = "ssrajamouli"
print(word_finder(name))