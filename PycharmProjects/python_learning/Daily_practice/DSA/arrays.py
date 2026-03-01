def target_value(arr, target):
    left = 0
    right = len(arr)-1

    while left<=right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid]<target:
            left = mid + 1
        else:
            right = mid - 1

    return -1

    
def reverse_array(arr):
    

arr = [2,4,6,8,10,12,14]
target = 6
print(target_value(arr,target))
print(reverse_array(arr))


