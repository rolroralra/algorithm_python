import random

import pytest

from algorithm.binarysearch.binarysearch import binarysearch


@pytest.mark.unit
class TestBinarySearchFound:
    @pytest.mark.parametrize("recursive", [False, True], ids=["iterative", "recursive"])
    @pytest.mark.parametrize("target", [1, 2, 3, 4, 5])
    def test_finds_existing_value(self, recursive, target):
        array = [1, 2, 3, 4, 5]
        assert array[binarysearch(array, target, recursive)] == target

    @pytest.mark.parametrize("recursive", [False, True], ids=["iterative", "recursive"])
    def test_single_element_array(self, recursive):
        assert binarysearch([42], 42, recursive) == 0


@pytest.mark.unit
class TestBinarySearchNotFound:
    @pytest.mark.parametrize("recursive", [False, True], ids=["iterative", "recursive"])
    def test_missing_value_returns_negative_insertion_point(self, recursive):
        array = [1, 3, 5, 7, 9]

        result = binarysearch(array, 4, recursive)

        insertion_point = -(result + 1)
        assert array[:insertion_point] + [4] + array[insertion_point:] == sorted(array + [4])

    @pytest.mark.parametrize("recursive", [False, True], ids=["iterative", "recursive"])
    def test_value_smaller_than_all_elements(self, recursive):
        assert binarysearch([1, 2, 3], 0, recursive) == -1

    @pytest.mark.parametrize("recursive", [False, True], ids=["iterative", "recursive"])
    def test_value_larger_than_all_elements(self, recursive):
        assert binarysearch([1, 2, 3], 10, recursive) == -4

    @pytest.mark.parametrize("recursive", [False, True], ids=["iterative", "recursive"])
    def test_empty_array(self, recursive):
        assert binarysearch([], 1, recursive) == -1


@pytest.mark.unit
class TestBinarySearchRandomized:
    @pytest.mark.parametrize("seed", range(10))
    def test_iterative_and_recursive_agree(self, seed):
        random.seed(seed)
        array = sorted(random.randint(0, 100) for _ in range(50))
        target = random.randint(-10, 110)

        assert binarysearch(array, target, False) == binarysearch(array, target, True)
