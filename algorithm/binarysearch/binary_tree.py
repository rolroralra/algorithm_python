from typing import Generic, Protocol, TypeVar, Callable

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
        self._inorder(self.root, lambda node: result.append(node.value))
        return result

    def preorder(self) -> list[T]:
        result: list[T] = []
        self._preorder(self.root, lambda node: result.append(node.value))
        return result

    def postorder(self) -> list[T]:
        result: list[T] = []
        self._postorder(self.root, lambda node: result.append(node.value))
        return result

    def height(self) -> int:
        return self._height(self.root)

    def print_tree(self):
        self._print_tree(self.root, '', True)

    def _inorder(self, node: BinaryTreeNode[T] | None,
        action: Callable[[T], None] = lambda x: print(x, end=' ')):
        if node is None:
            return

        self._inorder(node.left, action)
        action(node)
        self._inorder(node.right, action)

    def _preorder(self, node: BinaryTreeNode[T] | None,
        action: Callable[[T], None] = lambda x: print(x, end=' ')):
        if node is None:
            return

        action(node)
        self._preorder(node.left, action)
        self._preorder(node.right, action)

    def _postorder(self, node: BinaryTreeNode[T] | None,
        action: Callable[[T], None] = lambda x: print(x, end=' ')):
        if node is None:
            return

        self._postorder(node.left, action)
        self._postorder(node.right, action)
        action(node)

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

if __name__ == '__main__':
    class Node:
        def __init__(self, value):
            self.value = value
            self.left = None
            self.right = None

    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)
    root.left.left = Node(4)
    root.left.right = Node(5)

    tree = BinaryTree(root)
    print("Inorder traversal:", tree.inorder())
    print("Preorder traversal:", tree.preorder())
    print("Postorder traversal:", tree.postorder())
    print("Height of the tree:", tree.height())
    print("Tree structure:")
    tree.print_tree()