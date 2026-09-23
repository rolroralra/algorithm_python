import math
import random

import pytest

from algorithm.binarysearch.avl_tree import AVLNode, AVLTree


def assert_avl_balanced(node: AVLNode | None) -> int:
    """
    Recursively verify the AVL balance invariant (|left height - right height| <= 1)
    and that the cached `node.height` matches the actual subtree height.

    Returns:
        The height of the subtree rooted at `node` (0 for an empty subtree).
    """
    if node is None:
        return 0

    left_height = assert_avl_balanced(node.left)
    right_height = assert_avl_balanced(node.right)

    assert abs(left_height - right_height) <= 1, \
        f'balance factor violated at {node.value}: left={left_height}, right={right_height}'
    assert node.height == 1 + max(left_height, right_height)

    return node.height


@pytest.fixture
def avl_factory():
    def make(values: list[int] | None = None) -> AVLTree:
        return AVLTree(values)

    return make


@pytest.mark.unit
class TestAVLInsert:
    def test_inorder_stays_sorted_after_sorted_insert(self, avl_factory):
        avl = avl_factory(list(range(1, 51)))
        assert avl.inorder() == list(range(1, 51))

    def test_size_tracks_number_of_unique_values(self, avl_factory):
        avl = avl_factory([5, 3, 8, 3, 5])
        assert avl.size() == 3

    def test_duplicate_insert_is_ignored(self, avl_factory):
        avl = avl_factory([5])
        avl.insert(5)

        assert avl.size() == 1
        assert avl.inorder() == [5]

    def test_balance_invariant_holds_after_sorted_insert(self, avl_factory):
        avl = avl_factory(list(range(1, 200)))
        assert_avl_balanced(avl.root)

    @pytest.mark.parametrize("seed", range(5))
    def test_balance_invariant_holds_after_random_insert(self, avl_factory, seed):
        random.seed(seed)
        values = [random.randint(0, 1000) for _ in range(300)]

        avl = avl_factory(values)

        assert_avl_balanced(avl.root)
        assert avl.inorder() == sorted(set(values))

    def test_height_stays_logarithmic_for_sorted_insert(self, avl_factory):
        n = 1000
        avl = avl_factory(list(range(n)))

        # Known AVL bound: height <= 1.4404 * log2(n + 2) - 0.3277
        assert avl.height() <= 1.45 * math.log2(n + 2)


@pytest.mark.unit
class TestAVLDelete:
    def test_delete_leaf(self, avl_factory):
        avl = avl_factory([5, 3, 8])
        avl.delete(3)

        assert not avl.contains(3)
        assert avl.inorder() == [5, 8]

    def test_delete_missing_value_is_noop(self, avl_factory):
        avl = avl_factory([5, 3, 8])
        avl.delete(100)

        assert avl.size() == 3
        assert avl.inorder() == [3, 5, 8]

    def test_delete_all_empties_the_tree(self, avl_factory):
        values = [5, 3, 8, 1, 4, 7, 9]
        avl = avl_factory(values)

        for value in values:
            avl.delete(value)

        assert avl.is_empty()
        assert avl.root is None

    def test_balance_invariant_holds_after_deletes(self, avl_factory):
        avl = avl_factory(list(range(1, 200)))

        for value in range(1, 100):
            avl.delete(value)

        assert_avl_balanced(avl.root)
        assert avl.inorder() == list(range(100, 200))

    @pytest.mark.parametrize("seed", range(5))
    def test_balance_invariant_holds_after_random_insert_and_delete(self, avl_factory, seed):
        random.seed(seed)
        avl = avl_factory()
        inserted: list[int] = []

        for _ in range(300):
            if inserted and random.random() < 0.4:
                value = random.choice(inserted)
                avl.delete(value)
                inserted.remove(value)
            else:
                value = random.randint(0, 300)
                if not avl.contains(value):
                    avl.insert(value)
                    inserted.append(value)

            assert_avl_balanced(avl.root)
            assert avl.size() == len(inserted)

        assert avl.inorder() == sorted(inserted)


@pytest.mark.unit
class TestAVLQueries:
    def test_find_min_and_max(self, avl_factory):
        avl = avl_factory([5, 3, 8, 1, 9])

        assert avl.find_min() == 1
        assert avl.find_max() == 9

    def test_find_min_and_max_on_empty_tree(self, avl_factory):
        avl = avl_factory()

        assert avl.find_min() is None
        assert avl.find_max() is None

    def test_contains(self, avl_factory):
        avl = avl_factory([5, 3, 8])

        assert avl.contains(3) is True
        assert avl.contains(100) is False

    def test_custom_comparator(self):
        class Person:
            def __init__(self, name: str, age: int):
                self.name = name
                self.age = age

        people = [Person('Bob', 30), Person('Alice', 25), Person('Eve', 35)]
        avl = AVLTree(people, comp=lambda a, b: a.age - b.age)

        assert [p.age for p in avl.inorder()] == [25, 30, 35]
        assert avl.find_min().age == 25
        assert avl.find_max().age == 35
