def reverse_array(arr):
    left,right = 0,len(arr)-1

    while left<right:

        arr[left],arr[right] = arr[right],arr[left]
        left+=1
        right-=1
    return arr

insertion = [99,12,3,16,23,67]
print(reverse_array(insertion))