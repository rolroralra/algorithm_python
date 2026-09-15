import secrets

from algorithm.heap.heap import Heap

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

            # If no elements were swapped during the inner loop, the array is already sorted, and we can break early
            if not is_swapped:
                break

    @staticmethod
    def insertion_sort(array, comp=lambda a, b: a > b):
        size = len(array)
        for i in range(1, size):
            for j in range(i, 0, -1):
                # If the current element is not less than the previous element, we can break early since the array is already sorted up to this point
                if not comp(array[j - 1], array[j]):
                    break

                array[j - 1], array[j] = array[j], array[j - 1]

    @classmethod
    def merge_sort(cls, array, comp=lambda a, b: a > b):
        cls.__merge_sort(array, 0, len(array), comp)

    @classmethod
    def __merge_sort(cls, array, start_inclusive, end_exclusive, comp=lambda a, b: a > b):
        if end_exclusive - start_inclusive <= 1:
            return

        # Split the array into two halves and recursively sort each half
        mid = (start_inclusive + end_exclusive) // 2
        cls.__merge_sort(array, start_inclusive, mid, comp)
        cls.__merge_sort(array, mid, end_exclusive, comp)
        # Merge the two sorted halves
        cls.__merge(array, start_inclusive, mid, end_exclusive)

    @classmethod
    def __merge(cls, array, start_inclusive, mid, end_exclusive, comp=lambda a, b: a > b):
        i = start_inclusive
        j = mid
        k = 0

        merged_array = [0] * (end_exclusive - start_inclusive)

        # Merge the two sorted halves into a temporary array
        while i < mid and j < end_exclusive:
            if comp(array[i], array[j]):
                merged_array[k] = array[j]
                j += 1
            else:
                merged_array[k] = array[i]
                i += 1
            k += 1

        # Copy any remaining elements from the left half
        while i < mid:
            merged_array[k] = array[i]
            i += 1
            k += 1

        # Copy any remaining elements from the right half
        while j < end_exclusive:
            merged_array[k] = array[j]
            j += 1
            k += 1

        array[start_inclusive:end_exclusive] = merged_array[0:k]

    @classmethod
    def quick_sort(cls, array, comp=lambda a, b: a > b):
        cls.__quick_sort(array, 0, len(array), comp)

    @classmethod
    def __quick_sort(cls, array, start_inclusive, end_exclusive, comp=lambda a, b: a > b):
        if end_exclusive - start_inclusive <= 1:
            return

        # Randomly select a pivot index and partition the array around it
        final_pivot_index = cls.__partition_by_pivot_index(array, start_inclusive, end_exclusive, comp)
        # Recursively sort the subarrays on either side of the pivot
        cls.__quick_sort(array, start_inclusive, final_pivot_index)
        cls.__quick_sort(array, final_pivot_index + 1, end_exclusive)

    @classmethod
    def __partition_by_pivot_index(cls, array, start_inclusive, end_exclusive, comp=lambda a, b: a > b):
        # Randomly select a pivot index within the range [start_inclusive, end_exclusive)
        pivot_index = start_inclusive + secrets.randbelow(end_exclusive - start_inclusive)
        pivot = array[pivot_index]

        array[pivot_index], array[start_inclusive] = array[start_inclusive], array[pivot_index]

        # Partition the array such that elements less than the pivot are on the left and elements greater than the pivot are on the right
        index = start_inclusive
        for i in range(start_inclusive + 1, end_exclusive):
            if comp(pivot, array[i]):
                index += 1
                array[index], array[i] = array[i], array[index]

        array[start_inclusive], array[index] = array[index], array[start_inclusive]

        return index

    @staticmethod
    def heap_sort(array, comp=lambda a, b: a > b):
        Heap.heap_sort(array, comp)

    @staticmethod
    def counting_sort(array):
        if len(array) <= 1:
            return array

        min_val = min(array)
        max_val = max(array)
        value_size = max_val - min_val + 1

        if value_size > 1000000:
            raise ValueError("Counting sort is not suitable for large ranges of values.")

        count = [0] * value_size

        # Count the occurrences of each value in the input array
        for value in array:
            count[value - min_val] += 1

        # Cumulative count to determine the position of each element in the sorted array
        for i in range(1, value_size):
            count[i] += count[i - 1]

        sorted_array = [None] * len(array)

        # To maintain stability, we iterate through the original array in reverse order
        for value in reversed(array):
            count[value - min_val] -= 1
            sorted_array[count[value - min_val]] = value

        array[:] = sorted_array
        return array

    @classmethod
    def radix_sort(cls, array, base=10):
        if len(array) <= 1:
            return array

        if base < 2:
            raise ValueError("base must be at least 2.")

        min_val = min(array)
        max_val = max(array)
        max_shifted_value = max_val - min_val

        # Repeatedly sort by each digit, from least to most significant
        # The place_value variable represents the current digit's place (1 for units, 10 for tens, 100 for hundreds, etc.)
        place_value = 1
        while max_shifted_value // place_value > 0:
            cls.__counting_sort_by_digit(array, min_val, base, place_value)
            place_value *= base

        return array

    @staticmethod
    def __counting_sort_by_digit(array, min_val, base=10, place_value=1):
        size = len(array)
        count = [0] * base
        output = [None] * size

        # Count the occurrences of each digit (in the given base) at the current place value
        for value in array:
            digit = ((value - min_val) // place_value) % base
            count[digit] += 1

        # Cumulative count to determine the position of each element in the output array
        for i in range(1, base):
            count[i] += count[i - 1]

        # To maintain stability, we iterate through the array in reverse order
        for i in range(size - 1, -1, -1):
            digit = ((array[i] - min_val) // place_value) % base
            count[digit] -= 1
            output[count[digit]] = array[i]

        array[:] = output

    @staticmethod
    def bucket_sort(array):
        # TODO: implementation for bucket sort
        return

    @staticmethod
    def sort(array=None, comp=lambda a, b: a > b, algorithm=lambda arr, comp: Sort.quick_sort(arr, comp)):
        if array is None:
            return []

        cloned_array = array.copy()
        algorithm(cloned_array, comp)
        return cloned_array

    @staticmethod
    def sort(array=None, algorithm=lambda arr: Sort.counting_sort(arr)):
        if array is None:
            return []

        cloned_array = array.copy()
        algorithm(cloned_array)
        return cloned_array

    @staticmethod
    def swap(array, index1, index2):
        if index1 == index2:
            return

        temp = array[index1]
        array[index1] = array[index2]
        array[index2] = temp

import random

if __name__ == '__main__':
    array_size = 15
    original_list = [i + 1 for i in range(array_size)]
    random.shuffle(original_list)

    print(f"bubble sort    : {Sort.sort(original_list, algorithm=Sort.bubble_sort)}")

    print(f"selection sort : {Sort.sort(original_list, algorithm=Sort.selection_sort)}")

    print(f"insertion sort : {Sort.sort(original_list, algorithm=Sort.insertion_sort)}")

    print(f"merge sort     : {Sort.sort(original_list, algorithm=Sort.merge_sort)}")

    print(f"quick sort     : {Sort.sort(original_list, algorithm=Sort.quick_sort)}")

    print(f"heap sort      : {Sort.sort(original_list, algorithm=Sort.heap_sort)}")

    print(f"counting sort  : {Sort.sort(original_list, algorithm=Sort.counting_sort)}")

    print(f"radix sort     : {Sort.sort(original_list, algorithm=Sort.radix_sort)}")

    print(f"original array : {original_list}")
