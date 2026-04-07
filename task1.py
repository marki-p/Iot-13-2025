def quick_sort_0(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]

    left = [x for x in arr if x[0] < pivot[0]]
    middle = [x for x in arr if x[0] == pivot[0]]
    right = [x for x in arr if x[0] > pivot[0]]

    return quick_sort_0(left) + middle + quick_sort_0(right)

def map_cal(cal):
    sorted_cal = quick_sort_0(cal)
    mapped_cal = []
    current_0, current_1 = sorted_cal[0]
    
    for i in range(1, len(sorted_cal)):
        next_0, next_1 = sorted_cal [i]

        if next_0 <= current_1:
            if next_1 > current_1:
                current_1 = next_1
        else:
            mapped_cal.append((current_0, current_1))
            current_0, current_1 = next_0, next_1
    mapped_cal.append((current_0, current_1))

    return mapped_cal

