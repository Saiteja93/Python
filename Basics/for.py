n = 5
for i in range(1,n+1):
    pattern = ""
    for j in range(1,i+1):
        pattern+=str(j)
    print(pattern)

fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print(x)
  if x == "banana":
    break
  
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  if x == "banana":
    break
  print(x)