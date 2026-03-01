def number(n):
    for row in range(1,n+1):
        for j in range(row):
            print(row, end='')
        print()



def xmark_star(n):
    for row in range(1,n+1):
        for col in range(1,n+1):
            if row==col or row+col == n+1:
                print("*", end="")
            else:
                print(" ", end="")
        print() 

    print()   


def star_square(n):
    for row in range(1,n+1):
        for col in range(1,n+1):
            if row == 1 or row == n or col == 1 or col == n:
                print("*", end=" ")
            else:
                print(" ", end=" ")
        print()
    print()

n=5
number(n)
xmark_star(n)
star_square(n)

