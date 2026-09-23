import random

import pytest

from algorithm.heap.heap import Heap


@pytest.mark.unit
class TestHeapBasics:
    def test_new_heap_is_empty(self):
        heap = Heap()
        assert heap.is_empty()
        assert heap.size() == 0
        assert heap.peek() is None
        assert heap.pop() is None

    def test_add_and_peek(self):
        heap = Heap()
        heap.add(5)
        heap.add(1)
        heap.add(3)

        assert heap.peek() == 1
        assert heap.size() == 3

    def test_initializes_from_input_array(self):
        heap = Heap([5, 1, 3, 2, 4])
        assert heap.size() == 5
        assert heap.peek() == 1


@pytest.mark.unit
class TestHeapPopOrder:
    def test_default_comparator_pops_ascending(self):
        heap = Heap()
        for value in [3, 1, 4, 1, 5, 9, 2, 6]:
            heap.add(value)

        result = [heap.pop() for _ in range(heap.size())]
        assert result == sorted([3, 1, 4, 1, 5, 9, 2, 6])

    def test_reversed_comparator_pops_descending(self):
        heap = Heap(compare_function=lambda a, b: a < b)
        for value in [3, 1, 4, 1, 5, 9, 2, 6]:
            heap.add(value)

        result = []
        while not heap.is_empty():
            result.append(heap.pop())

        assert result == sorted([3, 1, 4, 1, 5, 9, 2, 6], reverse=True)

    def test_pop_empties_the_heap(self):
        heap = Heap([1, 2, 3])
        while not heap.is_empty():
            heap.pop()

        assert heap.is_empty()
        assert heap.pop() is None

    @pytest.mark.parametrize("seed", range(10))
    def test_matches_sorted_order_on_random_input(self, seed):
        random.seed(seed)
        values = [random.randint(-100, 100) for _ in range(60)]

        heap = Heap()
        for value in values:
            heap.add(value)

        popped = [heap.pop() for _ in range(len(values))]
        assert popped == sorted(values)


@pytest.mark.unit
class TestHeapSort:
    def test_sorts_ascending_by_default(self):
        array = [5, 3, 8, 1, 9, 2, 7]
        Heap.heap_sort(array)
        assert array == [1, 2, 3, 5, 7, 8, 9]

    def test_sorts_descending_with_custom_comparator(self):
        array = [5, 3, 8, 1, 9, 2, 7]
        Heap.heap_sort(array, comp=lambda a, b: a < b)
        assert array == [9, 8, 7, 5, 3, 2, 1]

    def test_empty_array(self):
        array = []
        Heap.heap_sort(array)
        assert array == []
