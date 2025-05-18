def upper_bound(sorted_array: list[int], target_value: int):
    """
    Returns the index of the first element greater than the given target in the sorted list.

    Parameters:
        sorted_array (list[int]): the sorted list
        target_value (int): the target value

    Returns:
        int: the index of the first element greater than the target
    """
    n = len(sorted_array)

    start_index = 0
    end_index = n - 1

    result = n
    while start_index <= end_index:
        mid_index = (start_index + end_index) // 2

        if sorted_array[mid_index] <= target_value:
            start_index = mid_index + 1
        else:
            end_index = mid_index - 1
            result = mid_index

    return result
