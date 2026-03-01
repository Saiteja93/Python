def number_pattern(n):
   
    for row in range(1,n+1):
      for s in range(n-row):
        print(" ", end='')
      for j in range(row):
        print(j+1, end="")
      print()
    print()

def inverted_number_two(n):
  for row in range(n):
    for s in range(row):
      print(" ",end='')

    num=n
    for j in range(n - row):
      print(num, end='')
      num-=1
  
    print()
  print()


def inverted_number_three(n):
  for row in range(n):
    for j in range(n-row, 0,-1):
      print(j, end="")
    print()
  print()  


def inverted_number_four(n):
  for row in range(1,n+1):
    num=row
    for j in range(row):
      
      print(num, end="")
      num+=1
      
    print()
  print()


def inverted_number_five(n):
  num=1
  for row in range(1,n+1):
    
    for j in range(row):
      print(num, end="")
      num+=1
      
   
    print()

      

n=5
number_pattern(n)
inverted_number_two(n)
inverted_number_three(n)
inverted_number_four(n)
inverted_number_five(n)



