from typing import Callable, Generic, TypeVar

from algorithm.binarysearch.binary_tree import BinaryTree

T = TypeVar('T')

DEFAULT_COMPARATOR: Callable[[T, T], int] = lambda a, b: (a > b) - (a < b)

RED = True
BLACK = False


class RBNode(Generic[T]):
    def __init__(self, value: T, color: bool = RED):
        self.value = value
        self.left: RBNode[T] | None = None
        self.right: RBNode[T] | None = None
        self.color = color


class RedBlackTree(BinaryTree[T], Generic[T]):
    """Left-leaning red-black tree (Sedgewick & Wayne)."""

    def __init__(self, input_array: list[T] | None = None, comp: Callable[[T, T], int] = DEFAULT_COMPARATOR):
        super().__init__()
        self.comp = comp
        self._size = 0

        if input_array:
            for value in input_array:
                self.insert(value)

    def insert(self, value: T):
        self.root = self._insert(self.root, value)
        self.root.color = BLACK

    def delete(self, value: T):
        if not self.contains(value):
            return

        if not self._is_red(self.root.left) and not self._is_red(self.root.right):
            self.root.color = RED

        self.root = self._delete(self.root, value)
        self._size -= 1

        if self.root is not None:
            self.root.color = BLACK

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

    def _insert(self, node: RBNode[T] | None, value: T) -> RBNode[T]:
        if node is None:
            self._size += 1
            return RBNode(value)

        comparison = self.comp(value, node.value)
        if comparison < 0:
            node.left = self._insert(node.left, value)
        elif comparison > 0:
            node.right = self._insert(node.right, value)
        else:
            return node

        return self._balance(node)

    def _delete(self, node: RBNode[T], value: T) -> RBNode[T] | None:
        if self.comp(value, node.value) < 0:
            if not self._is_red(node.left) and not self._is_red(node.left.left):
                node = self._move_red_left(node)
            node.left = self._delete(node.left, value)
        else:
            if self._is_red(node.left):
                node = self._rotate_right(node)
            if self.comp(value, node.value) == 0 and node.right is None:
                return None
            if not self._is_red(node.right) and not self._is_red(node.right.left):
                node = self._move_red_right(node)
            if self.comp(value, node.value) == 0:
                successor = self._find_min_node(node.right)
                node.value = successor.value
                node.right = self._delete_min(node.right)
            else:
                node.right = self._delete(node.right, value)

        return self._balance(node)

    def _delete_min(self, node: RBNode[T]) -> RBNode[T] | None:
        if node.left is None:
            return None

        if not self._is_red(node.left) and not self._is_red(node.left.left):
            node = self._move_red_left(node)

        node.left = self._delete_min(node.left)
        return self._balance(node)

    def _find(self, node: RBNode[T] | None, value: T) -> RBNode[T] | None:
        if node is None:
            return None

        comparison = self.comp(value, node.value)
        if comparison < 0:
            return self._find(node.left, value)
        elif comparison > 0:
            return self._find(node.right, value)
        return node

    @staticmethod
    def _find_min_node(node: RBNode[T]) -> RBNode[T]:
        while node.left is not None:
            node = node.left
        return node

    @staticmethod
    def _is_red(node: RBNode[T] | None) -> bool:
        return node is not None and node.color == RED

    def _rotate_left(self, node: RBNode[T]) -> RBNode[T]:
        new_root = node.right
        node.right = new_root.left
        new_root.left = node
        new_root.color = node.color
        node.color = RED
        return new_root

    def _rotate_right(self, node: RBNode[T]) -> RBNode[T]:
        new_root = node.left
        node.left = new_root.right
        new_root.right = node
        new_root.color = node.color
        node.color = RED
        return new_root

    @staticmethod
    def _flip_colors(node: RBNode[T]):
        node.color = not node.color
        node.left.color = not node.left.color
        node.right.color = not node.right.color

    def _balance(self, node: RBNode[T]) -> RBNode[T]:
        if self._is_red(node.right) and not self._is_red(node.left):
            node = self._rotate_left(node)
        if self._is_red(node.left) and self._is_red(node.left.left):
            node = self._rotate_right(node)
        if self._is_red(node.left) and self._is_red(node.right):
            self._flip_colors(node)

        return node

    def _move_red_left(self, node: RBNode[T]) -> RBNode[T]:
        self._flip_colors(node)
        if self._is_red(node.right.left):
            node.right = self._rotate_right(node.right)
            node = self._rotate_left(node)
            self._flip_colors(node)
        return node

    def _move_red_right(self, node: RBNode[T]) -> RBNode[T]:
        self._flip_colors(node)
        if self._is_red(node.left.left):
            node = self._rotate_right(node)
            self._flip_colors(node)
        return node


if __name__ == "__main__":
    # Same worst-case input as BinarySearchTree's demo: an already-sorted
    # array. A plain BST degenerates into a height-n linked list here, but
    # the red-black balance invariant (no root-to-leaf path is more than
    # twice as long as any other) keeps the height at O(log n).
    rbt = RedBlackTree(list(range(1, 11)))
    rbt.print_tree()
    print(rbt.inorder())
    print(f'sorted-order insert -> height: {rbt.height()} (n={rbt.size()})')

    rbt.insert(11)
    rbt.insert(0)
    rbt.delete(5)
    rbt.delete(9)
    rbt.print_tree()
    print(rbt.inorder())
    print(rbt.size())

    print(rbt.contains(8), rbt.contains(100))
    print(rbt.find_min(), rbt.find_max())

    class Person:
        def __init__(self, name: str, age: int):
            self.name = name
            self.age = age

        def __repr__(self):
            return f'{self.name}({self.age})'

    people = [Person('Bob', 30), Person('Alice', 25), Person('Eve', 35), Person('Carol', 28)]
    people_rbt = RedBlackTree(people, comp=lambda a, b: a.age - b.age)
    people_rbt.print_tree()
    print(people_rbt.inorder())

    people_rbt.delete(Person('', 30))
    print(people_rbt.inorder())
