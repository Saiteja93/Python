def insertion_sort(arr):
    n=len(arr)
    for i in range(1,n):
        key = arr[i]
        j = i - 1
        while j>=0 and arr[j] > key:
            arr[j+1] = arr[j]
            j -=1
        arr[j+1] = key
        
    return arr

 


insertion = [99,12,3,16,23,67]
print(insertion_sort(insertion))
print(reverse(insertion))