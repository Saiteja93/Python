s={"s":1,"a":2,"i":3}
h={"h":1,"s":2,"i":3,"t":4}

f=s.copy()
for key,value in h.items():
    if key in s:
        f[key]+=value
    else:
        f[key]=value
    
print(f)

