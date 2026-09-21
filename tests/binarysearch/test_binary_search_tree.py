import random

import pytest

from algorithm.binarysearch.binary_search_tree import BinarySearchTree, BSTNode


def assert_parent_consistency(node: BSTNode | None, expected_parent: BSTNode | None) -> None:
    if node is None:
        return

    assert node.parent is expected_parent
    assert_parent_consistency(node.left, node)
    assert_parent_consistency(node.right, node)


def force_loop_path(bst: BinarySearchTree) -> None:
    bst._size = 1000


@pytest.fixture(params=[False, True], ids=["recursive_path", "loop_path"])
def bst_factory(request):
    def make(values: list[int] | None = None) -> BinarySearchTree:
        bst = BinarySearchTree()
        if request.param:
            force_loop_path(bst)
        for value in values or []:
            bst.add(value)
        return bst

    return make


@pytest.mark.unit
class TestParentPointerOnInsert:
    def test_root_has_no_parent(self, bst_factory):
        bst = bst_factory([5])
        assert bst.root.parent is None

    def test_inserted_children_point_to_their_parent(self, bst_factory):
        bst = bst_factory([5, 3, 8, 1, 4, 7, 9])
        assert_parent_consistency(bst.root, None)

    def test_parent_consistency_after_sorted_insert(self, bst_factory):
        bst = bst_factory(list(range(1, 50)))
        assert_parent_consistency(bst.root, None)

    @pytest.mark.parametrize("seed", range(5))
    def test_parent_consistency_after_random_insert(self, bst_factory, seed):
        random.seed(seed)
        values = [random.randint(0, 200) for _ in range(150)]
        bst = bst_factory(values)
        assert_parent_consistency(bst.root, None)


@pytest.mark.unit
class TestParentPointerOnDelete:
    def test_delete_leaf_detaches_from_parent(self, bst_factory):
        bst = bst_factory([5, 3, 8])
        leaf = bst.search(3)
        parent = leaf.parent

        bst.remove(3)

        assert parent.left is None
        assert_parent_consistency(bst.root, None)

    def test_delete_node_with_one_child_relinks_parent(self, bst_factory):
        bst = bst_factory([5, 3, 8, 1])
        bst.remove(3)

        node = bst.search(1)
        assert node.parent is bst.root
        assert_parent_consistency(bst.root, None)

    def test_delete_node_with_two_children_relinks_parent(self, bst_factory):
        bst = bst_factory([5, 3, 8, 1, 4, 7, 9])
        bst.remove(5)

        assert_parent_consistency(bst.root, None)

    def test_delete_root_updates_new_root_parent(self, bst_factory):
        bst = bst_factory([5, 3, 8])
        bst.remove(5)

        assert bst.root.parent is None
        assert_parent_consistency(bst.root, None)

    @pytest.mark.parametrize("seed", range(5))
    def test_parent_consistency_after_random_insert_and_delete(self, bst_factory, seed):
        random.seed(seed)
        bst = bst_factory()
        inserted: list[int] = []

        for _ in range(200):
            if inserted and random.random() < 0.4:
                value = random.choice(inserted)
                bst.remove(value)
                inserted.remove(value)
            else:
                value = random.randint(0, 300)
                bst.add(value)
                if bst.contains(value):
                    inserted.append(value)

            assert_parent_consistency(bst.root, None)

        assert bst.inorder() == sorted(bst.inorder())


@pytest.mark.unit
class TestSuccessorPredecessor:
    def test_successor_uses_right_subtree_minimum(self, bst_factory):
        bst = bst_factory([5, 3, 8, 6, 9])
        node = bst.search(5)

        successor = bst.successor(node)

        assert successor.value == 6

    def test_predecessor_uses_left_subtree_maximum(self, bst_factory):
        bst = bst_factory([5, 3, 8, 2, 4])
        node = bst.search(5)

        predecessor = bst.predecessor(node)

        assert predecessor.value == 4

    def test_successor_climbs_to_ancestor_when_no_right_child(self, bst_factory):
        bst = bst_factory([5, 3, 8, 2, 4])
        node = bst.search(4)

        successor = bst.successor(node)

        assert successor.value == 5

    def test_predecessor_climbs_to_ancestor_when_no_left_child(self, bst_factory):
        bst = bst_factory([5, 3, 8, 6, 9])
        node = bst.search(6)

        predecessor = bst.predecessor(node)

        assert predecessor.value == 5

    def test_successor_of_maximum_is_none(self, bst_factory):
        bst = bst_factory([5, 3, 8, 2, 4, 6, 9])
        node = bst.search(bst.find_max())

        assert bst.successor(node) is None

    def test_predecessor_of_minimum_is_none(self, bst_factory):
        bst = bst_factory([5, 3, 8, 2, 4, 6, 9])
        node = bst.search(bst.find_min())

        assert bst.predecessor(node) is None

    def test_single_node_has_no_successor_or_predecessor(self, bst_factory):
        bst = bst_factory([42])
        node = bst.search(42)

        assert bst.successor(node) is None
        assert bst.predecessor(node) is None

    @pytest.mark.parametrize("seed", range(10))
    def test_successor_and_predecessor_match_sorted_order(self, bst_factory, seed):
        random.seed(seed)
        values = [random.randint(0, 500) for _ in range(random.randint(1, 100))]
        sorted_values = sorted(set(values))
        bst = bst_factory(values)

        for index, value in enumerate(sorted_values):
            node = bst.search(value)
            successor = bst.successor(node)
            predecessor = bst.predecessor(node)

            expected_successor = sorted_values[index + 1] if index + 1 < len(sorted_values) else None
            expected_predecessor = sorted_values[index - 1] if index > 0 else None

            assert (successor.value if successor else None) == expected_successor
            assert (predecessor.value if predecessor else None) == expected_predecessor
