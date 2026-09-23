from typing import Callable, Generic, TypeVar

from algorithm.binarysearch.binary_tree import BinaryTree, BinaryTreeNode

T = TypeVar('T')

DEFAULT_COMPARATOR: Callable[[T, T], int] = lambda a, b: (a > b) - (a < b)


class AVLNode(BinaryTreeNode[T], Generic[T]):
    left: 'AVLNode[T] | None'
    right: 'AVLNode[T] | None'

    def __init__(self, value: T):
        super().__init__(value)
        self.height = 1


class AVLTree(BinaryTree[T], Generic[T]):
    def __init__(self, input_array: list[T] | None = None, comp: Callable[[T, T], int] = DEFAULT_COMPARATOR):
        super().__init__()
        self.comp = comp
        self._size = 0

        if input_array:
            for value in input_array:
                self.insert(value)

    def insert(self, value: T):
        self.root = self._insert(self.root, value)

    def delete(self, value: T):
        self.root = self._delete(self.root, value)

    def contains(self, value: T) -> bool:
        return self._find(self.root, value) is not None

    def find_min(self) -> T | None:
        if self.root is None:
            return None
        return self._find_min_node(self.root).value

    def find_max(self) -> T | None:
        if self.root is None:
            return None

        node = self.root
        while node.right is not None:
            node = node.right
        return node.value

    def size(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self._size == 0

    def _insert(self, node: AVLNode[T] | None, value: T) -> AVLNode[T]:
        if node is None:
            self._size += 1
            return AVLNode(value)

        comparison = self.comp(value, node.value)
        if comparison < 0:
            node.left = self._insert(node.left, value)
        elif comparison > 0:
            node.right = self._insert(node.right, value)
        else:
            return node

        return self._rebalance(node)

    def _delete(self, node: AVLNode[T] | None, value: T) -> AVLNode[T] | None:
        if node is None:
            return None

        comparison = self.comp(value, node.value)
        if comparison < 0:
            node.left = self._delete(node.left, value)
        elif comparison > 0:
            node.right = self._delete(node.right, value)
        else:
            self._size -= 1

            if node.left is None:
                return node.right
            if node.right is None:
                return node.left

            successor = self._find_min_node(node.right)
            node.value = successor.value
            node.right = self._delete_min(node.right)

        return self._rebalance(node)

    def _delete_min(self, node: AVLNode[T]) -> AVLNode[T] | None:
        if node.left is None:
            return node.right

        node.left = self._delete_min(node.left)
        return self._rebalance(node)

    def _find(self, node: AVLNode[T] | None, value: T) -> AVLNode[T] | None:
        if node is None:
            return None

        comparison = self.comp(value, node.value)
        if comparison < 0:
            return self._find(node.left, value)
        elif comparison > 0:
            return self._find(node.right, value)
        return node

    @staticmethod
    def _find_min_node(node: AVLNode[T]) -> AVLNode[T]:
        while node.left is not None:
            node = node.left
        return node

    def _rebalance(self, node: AVLNode[T]) -> AVLNode[T]:
        self._update_height(node)
        balance_factor = self._balance_factor(node)

        if balance_factor > 1:
            if self._balance_factor(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        if balance_factor < -1:
            if self._balance_factor(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def _rotate_left(self, node: AVLNode[T]) -> AVLNode[T]:
        new_root = node.right
        node.right = new_root.left
        new_root.left = node
        self._update_height(node)
        self._update_height(new_root)
        return new_root

    def _rotate_right(self, node: AVLNode[T]) -> AVLNode[T]:
        new_root = node.left
        node.left = new_root.right
        new_root.right = node
        self._update_height(node)
        self._update_height(new_root)
        return new_root

    def _update_height(self, node: AVLNode[T]):
        node.height = 1 + max(self._node_height(node.left), self._node_height(node.right))

    def _balance_factor(self, node: AVLNode[T] | None) -> int:
        if node is None:
            return 0
        return self._node_height(node.left) - self._node_height(node.right)

    @staticmethod
    def _node_height(node: AVLNode[T] | None) -> int:
        return node.height if node is not None else 0


if __name__ == "__main__":
    # Same worst-case input as BinarySearchTree's demo: an already-sorted
    # array. A plain BST degenerates into a height-n linked list here, but
    # AVL's rotations keep the height within ~1.44 * log2(n) at all times.
    avl = AVLTree(list(range(1, 11)))
    avl.print_tree()
    print(avl.inorder())
    print(f'sorted-order insert -> height: {avl.height()} (n={avl.size()})')

    avl.insert(11)
    avl.insert(0)
    avl.delete(5)
    avl.delete(9)
    avl.print_tree()
    print(avl.inorder())
    print(avl.size())

    print(avl.contains(8), avl.contains(100))
    print(avl.find_min(), avl.find_max())

    class Person:
        def __init__(self, name: str, age: int):
            self.name = name
            self.age = age

        def __repr__(self):
            return f'{self.name}({self.age})'

    people = [Person('Bob', 30), Person('Alice', 25), Person('Eve', 35), Person('Carol', 28)]
    people_avl = AVLTree(people, comp=lambda a, b: a.age - b.age)
    people_avl.print_tree()
    print(people_avl.inorder())

    people_avl.delete(Person('', 30))
    print(people_avl.inorder())
