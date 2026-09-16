import random
from typing import Callable, Generic, TypeVar

from algorithm.binarysearch.binary_tree import BinaryTree

T = TypeVar('T')

DEFAULT_COMPARATOR: Callable[[T, T], int] = lambda a, b: (a > b) - (a < b)


class BSTNode(Generic[T]):
    def __init__(self, value: T):
        self.value = value
        self.left: BSTNode[T] | None = None
        self.right: BSTNode[T] | None = None


class BinarySearchTree(BinaryTree[T], Generic[T]):
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

    def _insert(self, node: BSTNode[T] | None, value: T) -> BSTNode[T]:
        if node is None:
            self._size += 1
            return BSTNode(value)

        comparison = self.comp(value, node.value)
        if comparison < 0:
            node.left = self._insert(node.left, value)
        elif comparison > 0:
            node.right = self._insert(node.right, value)

        return node

    def _delete(self, node: BSTNode[T] | None, value: T) -> BSTNode[T] | None:
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

        return node

    def _delete_min(self, node: BSTNode[T]) -> BSTNode[T] | None:
        if node.left is None:
            return node.right

        node.left = self._delete_min(node.left)
        return node

    def _find(self, node: BSTNode[T] | None, value: T) -> BSTNode[T] | None:
        if node is None:
            return None

        comparison = self.comp(value, node.value)
        if comparison < 0:
            return self._find(node.left, value)
        elif comparison > 0:
            return self._find(node.right, value)
        return node

    @staticmethod
    def _find_min_node(node: BSTNode[T]) -> BSTNode[T]:
        while node.left is not None:
            node = node.left
        return node


if __name__ == "__main__":
    bst = BinarySearchTree([5, 3, 8, 1, 4, 7, 9, 2, 6])
    bst.print_tree()
    print(bst.inorder())
    print(bst.size())

    bst.insert(10)
    bst.insert(0)
    print(bst.inorder())

    bst.delete(3)
    bst.delete(9)
    print(bst.inorder())
    print(bst.size())

    print(bst.contains(8), bst.contains(100))
    print(bst.find_min(), bst.find_max())

    class Person:
        def __init__(self, name: str, age: int):
            self.name = name
            self.age = age

        def __repr__(self):
            return f'{self.name}({self.age})'

    people = [Person('Bob', 30), Person('Alice', 25), Person('Eve', 35), Person('Carol', 28)]
    people_bst = BinarySearchTree(people, comp=lambda a, b: a.age - b.age)
    people_bst.print_tree()
    print(people_bst.inorder())

    people_bst.delete(Person('', 30))
    print(people_bst.inorder())

    # BST worst case: inserting an already-sorted array in order.
    # Every new value is greater than all existing ones, so each insert
    # only ever attaches to the rightmost node -> the tree degenerates
    # into a right-skewed linked list with height == n (O(n) search),
    # instead of the O(log n) height a balanced insertion order gives.
    sorted_array = list(range(1, 11))
    skewed_bst = BinarySearchTree(sorted_array)
    skewed_bst.print_tree()
    print(f'sorted-order insert -> height: {skewed_bst.height()} (n={skewed_bst.size()})')

    shuffled_array = sorted_array.copy()
    random.shuffle(shuffled_array)
    shuffled_bst = BinarySearchTree(shuffled_array)
    shuffled_bst.print_tree()
    print(f'shuffled-order insert -> height: {shuffled_bst.height()} (n={shuffled_bst.size()})')
