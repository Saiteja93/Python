def square_pattern(n):
    print("1.Square pattern: ")
    for row in range(1,n + 1):
        for star in range(n):
            print("*", end=" ")
        print()
    print()

def left_aligned_triangle(n):
    print("2.Left alignd triangle: ")
    for row in range(1,n+1):
        for star in range(row):
            print("*", end=" ")
        print()
    print()
    
def left_inverted_triangle(n):
    print("3.Left inverted triangle: ")
    for row in range(1,n+1):
        for star in range(n - row +1):
            print("*", end=" ")
        print()
    print()

def right_aligned_triangle(n):
    print("4.Right aligned triangle")
    for row in range(n+1):
        for space in range(n - row):
            print(' ', end=" ")

        for star in range(row):
            print("*", end=" ")
        print()
    print()



def right_aligned_inverted_triangle(n):
    print("\n5.Right aligned inverted traingle\n")
    digit = 1
    for row in range(1, n+1):
        for space in range(row - digit):
            print(" ", end=" ")
        for star in range(n - row + 1):
            print("*", end=" ")
        print()
    print()


def hallow_square(n):
    print("6.Hallow square\n")

    for row in range(1, n+1):
        if row == 1 or row == n:
            for star in range(1,n+1):
                print("*", end=" ")
            
                
        else:
            print("*",end=" ")
            for space in range(n-2):
                print(" ", end=" ")
            print("*", end="")
        print()

    print()

def pyramid(n):
    
    print("6.pyramid\n")
   
    for row in range(1,n+1):
        
        for space in range(n - row):
            print(" ", end=" ")

        for star in range(2 * row -1):
            
            print("*", end = " ")
            
         
        print()
    print()


def reverse_pyramid(n):
    print("7.Reverse pyramid\n")
    
    for row in range(n,0,-1):
        
        for space in range(n - row):
            print(" ", end=" ")
           
        for star in range(2 * row -1):
            print("*", end=" ")
        print()
    print()

def diamond(n):
    print("8. Diamond\n")
    for row in range(1,n+1):
        for space in range(n - row):
            print(" ", end="")
        for star in range(2 * row -1):
            print("*", end="")
        print()
    for row in range(n - 1,0,-1):
        for space in range(n - row):
            print(" ",end="")
        for star in range(2 * row -1):
            print("*", end="")
        print()

    print()







      

  
  
# Example
n = 5
p = 5
square_pattern(n)
left_aligned_triangle(n)
left_inverted_triangle(n)
right_aligned_triangle(n)
right_aligned_inverted_triangle(n)
hallow_square(n)
pyramid(p)
reverse_pyramid(p)
diamond(p)


