import random

import pytest

from algorithm.segment_tree.fenwick_tree.fenwick_tree import FenwickTree


def build_tree(values: list[int]) -> FenwickTree:
    """values is 0-indexed; the tree itself is 1-indexed."""
    tree = FenwickTree(len(values))
    for index, value in enumerate(values, start=1):
        tree.update(index, value)
    return tree


@pytest.mark.unit
class TestFenwickTree:
    def test_full_range_sum(self):
        tree = build_tree([1, 2, 3, 4, 5])
        assert tree.query(1, 5) == 15

    def test_partial_range_sum(self):
        tree = build_tree([1, 2, 3, 4, 5])
        assert tree.query(2, 4) == 9

    def test_single_index_query(self):
        tree = build_tree([1, 2, 3, 4, 5])
        assert tree.query(3, 3) == 3

    def test_update_adds_diff_instead_of_replacing(self):
        tree = build_tree([1, 2, 3, 4, 5])
        tree.update(3, 10)

        assert tree.query(3, 3) == 13
        assert tree.query(1, 5) == 25

    @pytest.mark.parametrize("seed", range(5))
    def test_matches_naive_prefix_sums(self, seed):
        random.seed(seed)
        values = [random.randint(-20, 20) for _ in range(20)]
        tree = build_tree(values)

        for _ in range(20):
            left = random.randint(1, 20)
            right = random.randint(left, 20)

            assert tree.query(left, right) == sum(values[left - 1:right])
