from sys import stdin

new_input = stdin.readline


def merge_sort(arr, left, right, expected_count):
    if left >= right:
        return 0, -1

    mid = (left + right) // 2

    c1, r1 = merge_sort(arr, left, mid, expected_count)
    if r1 != -1:
        return c1, r1

    c2, r2 = merge_sort(arr, mid + 1, right, expected_count - c1)
    if r2 != -1:
        return c1 + c2, r2

    c3, r3 = merge(arr, left, mid, right, expected_count - c1 - c2)
    if r3 != -1:
        return c1 + c2 + c3, r3

    return c1 + c2 + c3, -1


def merge(arr, left, mid, right, expected_count):
    tmp = [0] * (right - left + 1)

    left_index = left
    right_index = mid + 1
    tmp_index = 0
    while left_index <= mid and right_index <= right:
        if arr[left_index] <= arr[right_index]:
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

    count_result = 0
    result = -1
    for i in range(right - left + 1):
        arr[i + left] = tmp[i]
        count_result += 1

        if expected_count == count_result:
            result = tmp[i]

    return count_result, result


if __name__ == '__main__':
    n, k = map(int, new_input().split(" "))
    arr = list(map(int, new_input().split(" ")))

    count, result = merge_sort(arr, 0, len(arr) - 1, k)
    print(result)

