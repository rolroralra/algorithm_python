import bisect
import random

import pytest

from algorithm.binarysearch.upper_bound import upper_bound


@pytest.mark.unit
class TestUpperBound:
    def test_returns_index_after_last_matching_element(self):
        assert upper_bound([1, 2, 2, 2, 3], 2) == 4

    def test_target_smaller_than_all_elements_returns_zero(self):
        assert upper_bound([5, 6, 7], 1) == 0

    def test_target_larger_than_all_elements_returns_length(self):
        assert upper_bound([5, 6, 7], 10) == 3

    def test_target_between_elements_returns_next_greater_index(self):
        assert upper_bound([1, 3, 5, 7], 4) == 2

    def test_empty_array_returns_zero(self):
        assert upper_bound([], 5) == 0

    @pytest.mark.parametrize("seed", range(10))
    def test_matches_bisect_right(self, seed):
        random.seed(seed)
        array = sorted(random.randint(0, 20) for _ in range(50))
        target = random.randint(-5, 25)

        assert upper_bound(array, target) == bisect.bisect_right(array, target)
