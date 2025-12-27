
data = [1,2,2,4,5,6,6,6,7,7,8,8,8,9]
result = {}
for n in data:
    if n in result:
        result[n]+=1
    else:
        result[n]=1
print(result)

        
