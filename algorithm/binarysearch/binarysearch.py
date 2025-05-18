def binarysearch(sorted_array, target_value, recursive=False):
    if recursive:
        __binarysearch_by_recursive(sorted_array, target_value, 0, len(sorted_array) - 1)
    else:
        __binarysearch(sorted_array, target_value)

def __binarysearch(sorted_array, target_value):
    start_index = 0
    end_index = len(sorted_array) - 1

    while start_index <= end_index:
        mid_index = (start_index + end_index) // 2

        if sorted_array[mid_index] == target_value:
            return mid_index
        elif sorted_array[mid_index] < target_value:
            start_index = mid_index + 1
        else:
            end_index = mid_index - 1

    return -(start_index + 1)


def __binarysearch_by_recursive(sorted_array, target_value, start_index_inclusive, end_index_inclusive):
    if start_index_inclusive > end_index_inclusive:
        return -(start_index_inclusive + 1)

    mid_index = (start_index_inclusive + end_index_inclusive) // 2

    if sorted_array[mid_index] == target_value:
        return mid_index
    elif sorted_array[mid_index] > target_value:
        return __binarysearch_by_recursive(sorted_array, target_value, start_index_inclusive, mid_index - 1)
    else:
        return __binarysearch_by_recursive(sorted_array, target_value, mid_index + 1, end_index_inclusive)
