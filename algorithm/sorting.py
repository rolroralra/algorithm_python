class Sort:
    @staticmethod
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

    @staticmethod
    def bubble_sort(array, comp=lambda a, b: a > b):
        size = len(array)
        for i in range(size - 1):
            is_swapped = False
            for j in range(size - i - 1):
                if comp(array[j], array[j + 1]):
                    is_swapped = True
                    array[j], array[j + 1] = array[j + 1], array[j]

            if not is_swapped:
                break

    @staticmethod
    def insertion_sort(array, comp=lambda a, b: a > b):
        size = len(array)
        for i in range(1, size):
            for j in range(i, 0, -1):
                if not comp(array[j - 1], array[j]):
                    break

                array[j - 1], array[j] = array[j], array[j - 1]

    @classmethod
    def merge_sort(cls, array, comp=lambda a, b: a > b):
        cls.__merge_sort(array, 0, len(array), comp)

    @classmethod
    def __merge_sort(cls, array, start, end, comp=lambda a, b: a > b):
        if end - start <= 1:
            return

        mid = int((start + end) / 2)
        cls.__merge_sort(array, start, mid, comp)
        cls.__merge_sort(array, mid, end, comp)
        cls.__merge(array, start, mid, end)

    @classmethod
    def __merge(cls, array, start, mid, end, comp=lambda a, b: a > b):
        i = start
        j = mid
        k = 0

        merged_array = [0] * (end - start)

        while i < mid and j < end:
            if comp(array[i], array[j]):
                merged_array[k] = array[j]
                j += 1
            else:
                merged_array[k] = array[i]
                i += 1
            k += 1

        while i < mid:
            merged_array[k] = array[i]
            i += 1
            k += 1

        while j < end:
            merged_array[k] = array[j]
            j += 1
            k += 1

        array[start:end] = merged_array[0:k]

    @classmethod
    def quick_sort(cls, array, comp=lambda a, b: a > b):
        cls.__quick_sort(array, 0, len(array), comp)

    @classmethod
    def __quick_sort(cls, array, start, end, comp=lambda a, b: a > b):
        if end - start <= 1:
            return

        index = start
        for i in range(start, end):
            if comp(array[start], array[i]):
                index += 1
                array[index], array[i] = array[i], array[index]

        array[start], array[index] = array[index], array[start]
        cls.__quick_sort(array, start, index)
        cls.__quick_sort(array, index + 1, end)

    @staticmethod
    def heap_sort(array, comp=lambda a, b: a > b):
        return

    @staticmethod
    def counting_sort(array, comp=lambda a, b: a > b):
        return

    @staticmethod
    def radix_sort(array, comp=lambda a, b: a > b):
        return

    @staticmethod
    def sort(array=None, comp=lambda a, b: a > b, algorithm=lambda arr, comp: Sort.bubble_sort(arr, comp)):
        if array is None:
            return []

        cloned_array = array.copy()
        algorithm(cloned_array, comp)
        return cloned_array

    @staticmethod
    def swap(array, index1, index2):
        if index1 == index2:
            return

        temp = array[index1]
        array[index1] = array[index2]
        array[index2] = temp


if __name__ == '__main__':
    original_list = [8, 7, 6, 5, 4, 3, 2, 1]

    print(Sort.sort(original_list, algorithm=Sort.bubble_sort))

    print(Sort.sort(original_list, algorithm=Sort.selection_sort))

    print(Sort.sort(original_list, algorithm=Sort.insertion_sort))

    print(Sort.sort(original_list, algorithm=Sort.merge_sort))

    print(Sort.sort(original_list, algorithm=Sort.quick_sort))

    print(original_list)
