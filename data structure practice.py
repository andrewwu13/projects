def binary_search(arr, target):
    l = 0
    r = len(arr)
    while l <= r:
        mid = l + (r-l)//2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            l = mid + 1
        else:
            r = mid - 1


arr = [1, 2, 3, 5, 6, 7, 9, 11, 13, 14,
15, 18, 19, 21, 23, 25, 27, 29, 32, 34,
36, 37, 38, 40, 42, 44, 45, 47, 50, 52,
53, 58, 60, 62, 64, 66, 68, 70, 72, 75,
76, 81, 83, 85, 87, 91, 95, 96, 97, 99]

print(binary_search(arr,27))