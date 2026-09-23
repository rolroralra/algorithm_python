import pytest

from algorithm.binarysearch.binary_tree import BinaryTree, BinaryTreeNode


def build_sample_tree() -> BinaryTree:
    root = BinaryTreeNode(1)
    root.left = BinaryTreeNode(2)
    root.right = BinaryTreeNode(3)
    root.left.left = BinaryTreeNode(4)
    root.left.right = BinaryTreeNode(5)
    return BinaryTree(root)


@pytest.mark.unit
class TestBinaryTreeTraversal:
    def test_inorder(self):
        assert build_sample_tree().inorder() == [4, 2, 5, 1, 3]

    def test_preorder(self):
        assert build_sample_tree().preorder() == [1, 2, 4, 5, 3]

    def test_postorder(self):
        assert build_sample_tree().postorder() == [4, 5, 2, 3, 1]

    def test_empty_tree_traversals_are_empty(self):
        tree = BinaryTree()
        assert tree.inorder() == []
        assert tree.preorder() == []
        assert tree.postorder() == []


@pytest.mark.unit
class TestBinaryTreeHeight:
    def test_empty_tree_height_is_zero(self):
        assert BinaryTree().height() == 0

    def test_single_node_height_is_one(self):
        assert BinaryTree(BinaryTreeNode(1)).height() == 1

    def test_sample_tree_height(self):
        assert build_sample_tree().height() == 3

    def test_skewed_tree_height_matches_node_count(self):
        root = BinaryTreeNode(0)
        node = root
        for value in range(1, 5):
            node.right = BinaryTreeNode(value)
            node = node.right

        assert BinaryTree(root).height() == 5
