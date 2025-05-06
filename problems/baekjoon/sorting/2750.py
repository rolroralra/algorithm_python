def bubble_sort(array=None, comp=lambda a, b: a > b):
    if array is None:
        array = []

    size = len(array)
    for i in range(size - 1):
        is_swapped = False
        for j in range(size - i - 1):
            if comp(array[j], array[j + 1]):
                is_swapped = True
                swap(array, j, j + 1)

        if not is_swapped:
            break


def selection_sort(array, comp=lambda a, b: a > b):
    size = len(array)
    for i in range(size):
        selected_index = i
        selected_element = array[i]
        for j in range(i + 1, size):
            if comp(selected_element, array[j]):
                selected_index = j
                selected_element = array[j]

        array[i], array[selected_index] = array[selected_index], array[i]


def insertion_sort(array, comp=lambda a, b: a > b):
    size = len(array)
    for i in range(1, size):
        for j in range(i, 0, -1):
            if not comp(array[j - 1], array[j]):
                break

            array[j - 1], array[j] = array[j], array[j - 1]



def quick_sort(array, comp=lambda a, b: a > b):
    __quick_sort(array, 0, len(array), comp)


def __quick_sort(array, start_inclusive, end_exclusive, comp=lambda a, b: a > b):
    if end_exclusive - start_inclusive <= 1:
        return

    pivot_index = start_inclusive # can be modified in range (start_inclusive, end_inclusive)
    array[pivot_index], array[start_inclusive] = array[start_inclusive], array[pivot_index]

    index = start_inclusive
    for i in range(start_inclusive + 1, end_exclusive):
        if comp(array[start_inclusive], array[i]):
            index += 1
            array[index], array[i] = array[i], array[index]

    array[pivot_index], array[index] = array[index], array[pivot_index]
    __quick_sort(array, start_inclusive, index)
    __quick_sort(array, index + 1, end_exclusive)


def swap(array, index1, index2):
    array[index1], array[index2] = array[index2], array[index1]


if __name__ == '__main__':
    n = int(input())
    arr = []
    for i in range(n):
        arr.append(int(input()))

    selection_sort(arr)
    for value in arr:
        print(value)
