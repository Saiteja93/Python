

def sorting_number(arr):
    n=len(arr)

    for i in range(n):
        final= []
        for j in range(0,n-i-1):
           
            if arr[j] > arr[j+1]:
                arr[j],arr[j+1]=arr[j+1],arr[j]
    return arr






bubble = [5,6,9,1,4,2,3]
print(sorting_number(bubble))