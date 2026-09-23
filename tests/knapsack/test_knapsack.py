import pytest

from algorithm.knapsack.knapsack import knapsack


@pytest.mark.unit
class TestZeroOneKnapsack:
    def test_classic_example(self):
        weights = [2, 3, 4, 5]
        values = [3, 4, 5, 6]

        assert knapsack(weights, values, 5, one_or_zero=True) == 7

    def test_zero_capacity_yields_zero_value(self):
        assert knapsack([1, 2, 3], [10, 20, 30], 0, one_or_zero=True) == 0

    def test_cannot_take_item_twice(self):
        # Only one item of weight 5 fits; sufficient-stock variant could take it twice.
        weights = [5]
        values = [10]

        assert knapsack(weights, values, 10, one_or_zero=True) == 10

    def test_takes_all_items_when_capacity_allows(self):
        weights = [1, 2, 3]
        values = [10, 20, 30]

        assert knapsack(weights, values, 6, one_or_zero=True) == 60


@pytest.mark.unit
class TestUnboundedKnapsack:
    def test_reuses_best_item_to_fill_capacity(self):
        weights = [5]
        values = [10]

        assert knapsack(weights, values, 23, one_or_zero=False) == 40

    def test_zero_capacity_yields_zero_value(self):
        assert knapsack([1, 2, 3], [10, 20, 30], 0, one_or_zero=False) == 0

    def test_classic_example(self):
        weights = [1, 3, 4, 5]
        values = [1, 4, 5, 7]

        assert knapsack(weights, values, 7, one_or_zero=False) == 9


@pytest.mark.unit
class TestKnapsackValidation:
    def test_mismatched_lengths_raise(self):
        with pytest.raises(AssertionError):
            knapsack([1, 2], [1], 5)

    def test_negative_capacity_raises(self):
        with pytest.raises(AssertionError):
            knapsack([1], [1], -1)
