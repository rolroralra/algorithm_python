from typing import Generic, Protocol, TypeVar

T = TypeVar('T')


class BinaryTreeNode(Protocol[T]):
    value: T
    left: 'BinaryTreeNode[T] | None'
    right: 'BinaryTreeNode[T] | None'


class BinaryTree(Generic[T]):
    def __init__(self, root: BinaryTreeNode[T] | None = None):
        self.root = root

    def inorder(self) -> list[T]:
        result: list[T] = []
        self._inorder(self.root, result)
        return result

    def preorder(self) -> list[T]:
        result: list[T] = []
        self._preorder(self.root, result)
        return result

    def postorder(self) -> list[T]:
        result: list[T] = []
        self._postorder(self.root, result)
        return result

    def height(self) -> int:
        return self._height(self.root)

    def print_tree(self):
        self._print_tree(self.root, '', True)

    def _inorder(self, node: BinaryTreeNode[T] | None, result: list[T]):
        if node is None:
            return

        self._inorder(node.left, result)
        result.append(node.value)
        self._inorder(node.right, result)

    def _preorder(self, node: BinaryTreeNode[T] | None, result: list[T]):
        if node is None:
            return

        result.append(node.value)
        self._preorder(node.left, result)
        self._preorder(node.right, result)

    def _postorder(self, node: BinaryTreeNode[T] | None, result: list[T]):
        if node is None:
            return

        self._postorder(node.left, result)
        self._postorder(node.right, result)
        result.append(node.value)

    def _height(self, node: BinaryTreeNode[T] | None) -> int:
        if node is None:
            return 0

        return 1 + max(self._height(node.left), self._height(node.right))

    def _print_tree(self, node: BinaryTreeNode[T] | None, prefix: str, is_tail: bool):
        if node is None:
            return

        if node.right is not None:
            self._print_tree(node.right, prefix + ('│   ' if is_tail else '    '), False)

        print(prefix + ('└── ' if is_tail else '┌── ') + str(node.value))

        if node.left is not None:
            self._print_tree(node.left, prefix + ('    ' if is_tail else '│   '), True)
