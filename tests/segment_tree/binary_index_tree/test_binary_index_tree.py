import random

import pytest

from algorithm.segment_tree.binary_index_tree.binary_index_tree import SegmentTree


def build_tree(values: list[int]) -> SegmentTree:
    tree = SegmentTree(capacity=len(values))
    for index, value in enumerate(values):
        tree.update(index, value)
    return tree


@pytest.mark.unit
class TestBinaryIndexTree:
    def test_full_range_sum(self):
        tree = build_tree([1, 2, 3, 4, 5])
        assert tree.query(0, 4) == 15

    def test_partial_range_sum(self):
        tree = build_tree([1, 2, 3, 4, 5])
        assert tree.query(1, 3) == 9

    def test_single_index_query(self):
        tree = build_tree([1, 2, 3, 4, 5])
        assert tree.query(2, 2) == 3

    def test_update_changes_subsequent_queries(self):
        tree = build_tree([1, 2, 3, 4, 5])
        tree.update(2, 100)

        assert tree.query(0, 4) == 1 + 2 + 100 + 4 + 5

    @pytest.mark.parametrize("seed", range(5))
    def test_matches_naive_prefix_sums(self, seed):
        random.seed(seed)
        values = [random.randint(-20, 20) for _ in range(20)]
        tree = build_tree(values)

        for _ in range(20):
            left = random.randint(0, 19)
            right = random.randint(left, 19)

            assert tree.query(left, right) == sum(values[left:right + 1])
