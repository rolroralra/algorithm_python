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


def selection_sort(array=None, comp=lambda a, b: a > b):
    if array is None:
        array = []




def swap(array, index1, index2):
    temp = array[index1]
    array[index1] = array[index2]
    array[index2] = array[index1]


if __name__ == '__main__':
    n = int(input())
    arr = []
    for i in range(n):
        arr.append(int(input()))

    bubble_sort(arr)
    for value in arr:
        print(value)
