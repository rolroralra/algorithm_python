import pytest

from algorithm.segment_tree.segment_tree import SegmentTree


def build_sum_tree(values: list[int]) -> SegmentTree:
    tree = SegmentTree(len(values))
    for index, value in enumerate(values):
        tree.update(index, value)
    return tree


@pytest.mark.unit
class TestSegmentTreeSumQuery:
    def test_full_range_sum(self):
        tree = build_sum_tree([1, 2, 3, 4, 5])
        assert tree.query(0, 4) == 15

    def test_partial_range_sum(self):
        tree = build_sum_tree([1, 2, 3, 4, 5])
        assert tree.query(1, 3) == 9

    def test_single_element_range(self):
        tree = build_sum_tree([1, 2, 3, 4, 5])
        assert tree.query(2, 2) == 3

    def test_update_changes_subsequent_queries(self):
        tree = build_sum_tree([1, 2, 3, 4, 5])
        tree.update(2, 100)

        assert tree.query(0, 4) == 1 + 2 + 100 + 4 + 5
        assert tree.query(2, 2) == 100

    def test_non_power_of_two_size(self):
        tree = build_sum_tree([1, 2, 3])
        assert tree.query(0, 2) == 6
        assert tree.query(0, 1) == 3


@pytest.mark.unit
class TestSegmentTreeMinOperator:
    def test_finds_minimum_in_range(self):
        tree = SegmentTree(5, min, float("inf"))
        for index, value in enumerate([5, 3, 8, 1, 9]):
            tree.update(index, value)

        assert tree.query(0, 4) == 1
        assert tree.query(0, 1) == 3
        assert tree.query(3, 4) == 1

    def test_update_reflected_in_minimum(self):
        tree = SegmentTree(5, min, float("inf"))
        for index, value in enumerate([5, 3, 8, 1, 9]):
            tree.update(index, value)

        tree.update(3, 100)

        assert tree.query(0, 4) == 3


@pytest.mark.unit
class TestSegmentTreeMaxOperator:
    def test_finds_maximum_in_range(self):
        tree = SegmentTree(5, max, float("-inf"))
        for index, value in enumerate([5, 3, 8, 1, 9]):
            tree.update(index, value)

        assert tree.query(0, 4) == 9
        assert tree.query(0, 2) == 8
