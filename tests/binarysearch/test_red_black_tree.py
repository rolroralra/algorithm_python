import random

import pytest

from algorithm.binarysearch.red_black_tree import BLACK, RBNode, RED, RedBlackTree


def assert_llrb_invariants(node: RBNode | None) -> int:
    """
    Recursively verify the left-leaning red-black invariants:
      - no red right link (a red link only ever leans left)
      - no two consecutive red links (a red node has no red child)
      - every root-to-None path has the same black-height (perfect black balance)

    Returns:
        The black-height of the subtree rooted at `node` (None counts as 1 black link,
        the usual convention for measuring black-height).
    """
    if node is None:
        return 1

    assert node.right is None or node.right.color == BLACK, \
        f'red link leans right at {node.value}'

    if node.color == RED:
        assert node.left is None or node.left.color == BLACK, \
            f'two consecutive red links at {node.value}'

    left_black_height = assert_llrb_invariants(node.left)
    right_black_height = assert_llrb_invariants(node.right)

    assert left_black_height == right_black_height, \
        f'black-height mismatch at {node.value}: left={left_black_height}, right={right_black_height}'

    return left_black_height + (0 if node.color == RED else 1)


@pytest.fixture
def rbt_factory():
    def make(values: list[int] | None = None) -> RedBlackTree:
        return RedBlackTree(values)

    return make


@pytest.mark.unit
class TestRedBlackTreeInsert:
    def test_inorder_stays_sorted_after_sorted_insert(self, rbt_factory):
        rbt = rbt_factory(list(range(1, 51)))
        assert rbt.inorder() == list(range(1, 51))

    def test_root_is_always_black(self, rbt_factory):
        rbt = rbt_factory([5, 3, 8, 1, 4, 7, 9])
        assert rbt.root.color == BLACK

    def test_size_tracks_number_of_unique_values(self, rbt_factory):
        rbt = rbt_factory([5, 3, 8, 3, 5])
        assert rbt.size() == 3

    def test_duplicate_insert_is_ignored(self, rbt_factory):
        rbt = rbt_factory([5])
        rbt.insert(5)

        assert rbt.size() == 1
        assert rbt.inorder() == [5]

    def test_llrb_invariants_hold_after_sorted_insert(self, rbt_factory):
        rbt = rbt_factory(list(range(1, 200)))
        assert_llrb_invariants(rbt.root)

    @pytest.mark.parametrize("seed", range(5))
    def test_llrb_invariants_hold_after_random_insert(self, rbt_factory, seed):
        random.seed(seed)
        values = [random.randint(0, 1000) for _ in range(300)]

        rbt = rbt_factory(values)

        assert_llrb_invariants(rbt.root)
        assert rbt.inorder() == sorted(set(values))


@pytest.mark.unit
class TestRedBlackTreeDelete:
    def test_delete_leaf(self, rbt_factory):
        rbt = rbt_factory([5, 3, 8])
        rbt.delete(3)

        assert not rbt.contains(3)
        assert rbt.inorder() == [5, 8]

    def test_delete_missing_value_is_noop(self, rbt_factory):
        rbt = rbt_factory([5, 3, 8])
        rbt.delete(100)

        assert rbt.size() == 3
        assert rbt.inorder() == [3, 5, 8]

    def test_delete_all_empties_the_tree(self, rbt_factory):
        values = [5, 3, 8, 1, 4, 7, 9]
        rbt = rbt_factory(values)

        for value in values:
            rbt.delete(value)

        assert rbt.is_empty()
        assert rbt.root is None

    def test_llrb_invariants_hold_after_deletes(self, rbt_factory):
        rbt = rbt_factory(list(range(1, 200)))

        for value in range(1, 100):
            rbt.delete(value)

        assert_llrb_invariants(rbt.root)
        assert rbt.inorder() == list(range(100, 200))

    @pytest.mark.parametrize("seed", range(5))
    def test_llrb_invariants_hold_after_random_insert_and_delete(self, rbt_factory, seed):
        random.seed(seed)
        rbt = rbt_factory()
        inserted: list[int] = []

        for _ in range(300):
            if inserted and random.random() < 0.4:
                value = random.choice(inserted)
                rbt.delete(value)
                inserted.remove(value)
            else:
                value = random.randint(0, 300)
                if not rbt.contains(value):
                    rbt.insert(value)
                    inserted.append(value)

            assert_llrb_invariants(rbt.root)
            assert rbt.size() == len(inserted)

        assert rbt.inorder() == sorted(inserted)


@pytest.mark.unit
class TestRedBlackTreeQueries:
    def test_find_min_and_max(self, rbt_factory):
        rbt = rbt_factory([5, 3, 8, 1, 9])

        assert rbt.find_min() == 1
        assert rbt.find_max() == 9

    def test_find_min_and_max_on_empty_tree(self, rbt_factory):
        rbt = rbt_factory()

        assert rbt.find_min() is None
        assert rbt.find_max() is None

    def test_contains(self, rbt_factory):
        rbt = rbt_factory([5, 3, 8])

        assert rbt.contains(3) is True
        assert rbt.contains(100) is False

    def test_custom_comparator(self):
        class Person:
            def __init__(self, name: str, age: int):
                self.name = name
                self.age = age

        people = [Person('Bob', 30), Person('Alice', 25), Person('Eve', 35)]
        rbt = RedBlackTree(people, comp=lambda a, b: a.age - b.age)

        assert [p.age for p in rbt.inorder()] == [25, 30, 35]
        assert rbt.find_min().age == 25
        assert rbt.find_max().age == 35
