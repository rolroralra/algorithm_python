from problems.baekjoon.dfs import 2023
def binarysearch(arr, target, recursive=False):
    if recursive:
        __binarysearch_by_recursive(arr, target, 0, len(arr) - 1)
    else:
        __binarysearch(arr, target)

def __binarysearch(arr, target):
    start_index = 0
    end_index = len(arr) - 1

    while start_index <= end_index:
        mid_index = (start_index + end_index) // 2

        if arr[mid_index] == target:
            return mid_index
        elif arr[mid_index] < target:
            start_index = mid_index + 1
        else:
            end_index = mid_index - 1

    return -(start_index + 1)


def __binarysearch_by_recursive(arr, target, start_index, end_index):
    if start_index > end_index:
        return -(start_index + 1)

    mid_index = (start_index + end_index) // 2

    if arr[mid_index] == target:
        return mid_index
    elif arr[mid_index] > target:
        return __binarysearch_by_recursive(arr, target, start_index, mid_index - 1)
    else:
        return __binarysearch_by_recursive(arr, target, mid_index + 1, end_index)
