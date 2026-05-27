names=["sai", "teja", "john", "david","hinge"]

def name_dict(names):
    final = {}
    for name in names:
        for s in name:
            if s in final:
                final[s]+=1
            else:final[s]=1
    return final

numbering = name_dict(names)
print(numbering)

