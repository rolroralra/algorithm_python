import heapq

def selection_sort(arr, left, right, comp):
    for i in range(left, right):
        min_index = i
        min_value = arr[i]
        for j in range(i + 1, right + 1):
            if comp(min_value, arr[j]) > 0:
                min_index = j
                min_value = arr[j]

        if i != min_index:
            arr[i], arr[min_index] = arr[min_index], arr[i]


def insertion_sort(arr, left, right, comp):
    for i in range(left + 1, right + 1):
        for j in range(i, left, -1):
            if comp(arr[j - 1], arr[j]) <= 0:
                break

            arr[j - 1], arr[j] = arr[j], arr[j - 1]


def bubble_sort(arr, left, right, comp):
    for i in range(right - left):
        is_swapped = False
        for j in range(left, right - i):
            if comp(arr[j], arr[j + 1]) > 0:
                is_swapped = True
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

        if not is_swapped:
            break


def quick_sort(arr, left, right, comp):
    if left >= right:
        return

    pivot = left
    index = left
    for i in range(left + 1, right + 1):
        if comp(arr[pivot], arr[i]) > 0:
            index += 1
            if i != index:
                arr[index], arr[i] = arr[i], arr[index]

    arr[pivot], arr[index] = arr[index], arr[pivot]

    quick_sort(arr, left, index - 1, comp)
    quick_sort(arr, index + 1, right, comp)


def merge_sort(arr, left, right, comp):
    if left >= right:
        return

    mid = (left + right) // 2
    merge_sort(arr, left, mid, comp)
    merge_sort(arr, mid + 1, right, comp)
    merge(arr, left, mid, right, comp)


def merge(arr, left, mid, right, comp):
    left_index = left
    right_index = mid + 1

    tmp = [0] * (right - left + 1)
    tmp_index = 0

    while left_index <= mid and right_index <= right:
        if comp(arr[left_index], arr[right_index]) <= 0:
            tmp[tmp_index] = arr[left_index]
            left_index += 1
        else:
            tmp[tmp_index] = arr[right_index]
            right_index += 1

        tmp_index += 1

    while left_index <= mid:
        tmp[tmp_index] = arr[left_index]
        left_index += 1
        tmp_index += 1

    while right_index <= right:
        tmp[tmp_index] = arr[right_index]
        right_index += 1
        tmp_index += 1

    for i in range(right - left + 1):
        arr[left + i] = tmp[i]


def heap_sort(arr, left, right, comp):
    tmp = []
    heapq.heapify(tmp)
    for v in arr:
        heapq.heappush(tmp, v)

    for i in range(left, right + 1):
        arr[i] = heapq.heappop(tmp)

    if comp(0, 1) > 0:
        arr = arr.reverse()


def test_sort(arr, sort, comp=lambda x, y: x - y):
    test_arr = arr.copy()
    sort(test_arr, 0, len(test_arr) - 1, comp)
    print(test_arr)


if __name__ == '__main__':
    arr = [5, 2, 10, 4, 8, 1, 6, 9, 3, 7]

    test_sort(arr, selection_sort)
    test_sort(arr, insertion_sort)
    test_sort(arr, bubble_sort)
    test_sort(arr, quick_sort)
    test_sort(arr, merge_sort)
    test_sort(arr, heap_sort)

    comp = lambda x, y: y - x

    test_sort(arr, selection_sort, comp)
    test_sort(arr, insertion_sort, comp)
    test_sort(arr, bubble_sort, comp)
    test_sort(arr, quick_sort, comp)
    test_sort(arr, merge_sort, comp)
    test_sort(arr, heap_sort, comp)
