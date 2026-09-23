import random

import pytest

from algorithm.sort.sorting import Sort

IN_PLACE_ALGORITHMS = {
    "selection_sort": Sort.selection_sort,
    "bubble_sort": Sort.bubble_sort,
    "insertion_sort": Sort.insertion_sort,
    "shell_sort": Sort.shell_sort,
    "merge_sort": Sort.merge_sort,
    "quick_sort": Sort.quick_sort,
    "heap_sort": Sort.heap_sort,
    # bucket_sort distributes by value magnitude, but sorts each bucket with
    # insertion_sort, so it is comparison-based just like the others here.
    "bucket_sort": Sort.bucket_sort,
}

NON_COMPARISON_ALGORITHMS = {
    "counting_sort": Sort.counting_sort,
    "radix_sort": Sort.radix_sort,
}


@pytest.mark.unit
class TestComparisonBasedSorts:
    @pytest.mark.parametrize("algorithm", IN_PLACE_ALGORITHMS.values(), ids=IN_PLACE_ALGORITHMS.keys())
    def test_sorts_ascending_by_default(self, algorithm):
        array = [5, 3, 8, 1, 9, 2, 7]
        algorithm(array)
        assert array == [1, 2, 3, 5, 7, 8, 9]

    @pytest.mark.parametrize("algorithm", IN_PLACE_ALGORITHMS.values(), ids=IN_PLACE_ALGORITHMS.keys())
    def test_sorts_descending_with_custom_comparator(self, algorithm):
        array = [5, 3, 8, 1, 9, 2, 7]
        algorithm(array, comp=lambda a, b: a < b)
        assert array == [9, 8, 7, 5, 3, 2, 1]

    @pytest.mark.parametrize("algorithm", IN_PLACE_ALGORITHMS.values(), ids=IN_PLACE_ALGORITHMS.keys())
    def test_empty_array(self, algorithm):
        array = []
        algorithm(array)
        assert array == []

    @pytest.mark.parametrize("algorithm", IN_PLACE_ALGORITHMS.values(), ids=IN_PLACE_ALGORITHMS.keys())
    def test_single_element_array(self, algorithm):
        array = [42]
        algorithm(array)
        assert array == [42]

    @pytest.mark.parametrize("algorithm", IN_PLACE_ALGORITHMS.values(), ids=IN_PLACE_ALGORITHMS.keys())
    def test_array_with_duplicates(self, algorithm):
        array = [4, 2, 4, 1, 2, 4]
        algorithm(array)
        assert array == [1, 2, 2, 4, 4, 4]

    @pytest.mark.parametrize("algorithm", IN_PLACE_ALGORITHMS.values(), ids=IN_PLACE_ALGORITHMS.keys())
    @pytest.mark.parametrize("seed", range(10))
    def test_matches_builtin_sorted_on_random_input(self, algorithm, seed):
        random.seed(seed)
        array = [random.randint(-50, 50) for _ in range(60)]
        expected = sorted(array)

        algorithm(array)

        assert array == expected


@pytest.mark.unit
class TestNonComparisonSorts:
    @pytest.mark.parametrize("algorithm", NON_COMPARISON_ALGORITHMS.values(), ids=NON_COMPARISON_ALGORITHMS.keys())
    def test_sorts_ascending(self, algorithm):
        array = [5, 3, 8, 1, 9, 2, 7]
        result = algorithm(array)
        assert result == [1, 2, 3, 5, 7, 8, 9]
        assert array == [1, 2, 3, 5, 7, 8, 9]

    @pytest.mark.parametrize("algorithm", NON_COMPARISON_ALGORITHMS.values(), ids=NON_COMPARISON_ALGORITHMS.keys())
    def test_empty_array(self, algorithm):
        assert algorithm([]) == []

    @pytest.mark.parametrize("algorithm", NON_COMPARISON_ALGORITHMS.values(), ids=NON_COMPARISON_ALGORITHMS.keys())
    def test_single_element_array(self, algorithm):
        assert algorithm([7]) == [7]

    @pytest.mark.parametrize("algorithm", NON_COMPARISON_ALGORITHMS.values(), ids=NON_COMPARISON_ALGORITHMS.keys())
    def test_array_with_negative_numbers(self, algorithm):
        array = [-3, 5, -1, 0, 2, -8]
        assert algorithm(array) == sorted(array)

    @pytest.mark.parametrize("algorithm", NON_COMPARISON_ALGORITHMS.values(), ids=NON_COMPARISON_ALGORITHMS.keys())
    @pytest.mark.parametrize("seed", range(10))
    def test_matches_builtin_sorted_on_random_input(self, algorithm, seed):
        random.seed(seed)
        array = [random.randint(-50, 50) for _ in range(60)]

        assert algorithm(array) == sorted(array)

    def test_counting_sort_rejects_huge_value_range(self):
        with pytest.raises(ValueError):
            Sort.counting_sort([0, 2_000_000])

    def test_radix_sort_rejects_invalid_base(self):
        with pytest.raises(ValueError):
            Sort.radix_sort([1, 2, 3], base=1)


@pytest.mark.unit
class TestSortDispatcher:
    def test_none_array_returns_empty_list(self):
        assert Sort.sort(None) == []

    def test_default_algorithm_is_ascending_quick_sort(self):
        assert Sort.sort([3, 1, 2]) == [1, 2, 3]

    def test_does_not_mutate_input_array(self):
        original = [3, 1, 2]
        result = Sort.sort(original, algorithm=Sort.merge_sort)

        assert result == [1, 2, 3]
        assert original == [3, 1, 2]

    def test_dispatches_to_comparison_algorithm(self):
        assert Sort.sort([3, 1, 2], algorithm=Sort.bubble_sort) == [1, 2, 3]

    def test_dispatches_to_non_comparison_algorithm(self):
        assert Sort.sort([3, 1, 2], algorithm=Sort.counting_sort) == [1, 2, 3]

    def test_dispatches_with_custom_comparator(self):
        result = Sort.sort([3, 1, 2], comp=lambda a, b: a < b, algorithm=Sort.selection_sort)
        assert result == [3, 2, 1]


@pytest.mark.unit
class TestSwap:
    def test_swaps_two_different_indices(self):
        array = [1, 2, 3]
        Sort.swap(array, 0, 2)
        assert array == [3, 2, 1]

    def test_swapping_same_index_is_noop(self):
        array = [1, 2, 3]
        Sort.swap(array, 1, 1)
        assert array == [1, 2, 3]
