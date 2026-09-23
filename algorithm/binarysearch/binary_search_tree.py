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
        self.parent: BSTNode[T] | None = None

    def is_leaf(self) -> bool:
        return self.left is None and self.right is None

    def is_internal(self) -> bool:
        return not self.is_leaf()

    def is_root(self) -> bool:
        return self.parent is None

    def is_left_child(self) -> bool:
        return self.parent is not None and self is self.parent.left

    def is_right_child(self) -> bool:
        return self.parent is not None and self is self.parent.right

    def has_left_child(self) -> bool:
        return self.left is not None

    def has_right_child(self) -> bool:
        return self.right is not None

    def set_left(self, child: 'BSTNode[T] | None') -> None:
        self.left = child
        if child is not None:
            child.parent = self

    def set_right(self, child: 'BSTNode[T] | None') -> None:
        self.right = child
        if child is not None:
            child.parent = self


class BinarySearchTree(BinaryTree[T], Generic[T]):
    def __init__(self, input_array: list[T] | None = None, comp: Callable[[T, T], int] = DEFAULT_COMPARATOR):
        super().__init__()
        self.comp = comp
        self._size = 0

        if input_array:
            for value in input_array:
                self.add(value)

    def add(self, value: T):
        self._insert(value)

    def remove(self, value: T):
        self._delete(value)

    def find(self, value: T) -> BSTNode[T] | None:
        return self._find(self.root, value)

    def contains(self, value: T) -> bool:
        return self._find(self.root, value) is not None

    def find_min(self) -> T | None:
        if self.root is None:
            return None
        return self.find_min_node(self.root).value

    def find_max(self) -> T | None:
        if self.root is None:
            return None

        return self.find_max_node(self.root).value

    def find_leaf_node_having_value(self, value: T) -> tuple[BSTNode[T] | None, int]:
        """
        self.root에서 시작해 value가 들어갈 위치의 부모 노드를 찾는다.

        Returns:
            (parent, comparison) 튜플.
            - comparison == 0 이면 parent는 동일한 값을 가진 기존 노드 (중복).
            - 그 외에는 parent가 새 노드를 붙일 부모, comparison 부호가 left/right 방향.
        """
        parent, current = None, self.root
        comparison = 0
        while current is not None:
            comparison = self.comp(value, current.value)
            if comparison == 0:
                return current, 0

            parent = current
            current = current.left if comparison < 0 else current.right

        return parent, comparison

    def size(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self._size == 0

    def _find(self, node: BSTNode[T] | None, value: T) -> BSTNode[T] | None:
        if self.size() < 1000:
            return self._find_by_recursive(node, value)

        return self._find_by_loop(node, value)

    def _find_by_loop(self, node: BSTNode[T] | None, value: T) -> BSTNode[T] | None:
        if node is None:
            return None

        while node is not None:
            comparison = self.comp(value, node.value)
            if comparison < 0:
                node = node.left
            elif comparison > 0:
                node = node.right
            else:
                return node

        return None

    def _find_by_recursive(self, node: BSTNode[T] | None, value: T) -> BSTNode[T] | None:
        if node is None:
            return None

        comparison = self.comp(value, node.value)
        if comparison < 0:
            return self._find_by_recursive(node.left, value)
        elif comparison > 0:
            return self._find_by_recursive(node.right, value)
        return node

    def _insert(self, value: T):
        if self.size() < 1000:
            self.root = self._insert_by_recursive(self.root, value)
        else:
            self._insert_by_loop(value)

    def _insert_by_recursive(self, node: BSTNode[T] | None, value: T) -> BSTNode[T]:
        """
        Args:
            node: root node of the BST
            value: value to be inserted into the BST

        Returns: root node of the BST after insertion
        """
        # Leaf node reached, insert the new value here
        if node is None:
            self._increase_size()
            return BSTNode(value)

        comparison = self.comp(value, node.value)
        if comparison < 0:
            node.set_left(self._insert_by_recursive(node.left, value))
        elif comparison > 0:
            node.set_right(self._insert_by_recursive(node.right, value))

        return node

    def _insert_by_loop(self, value: T) -> None:
        if self.root is None:
            self._increase_size()
            self.root = BSTNode(value)
            return

        leaf_node, _comparison = self.find_leaf_node_having_value(value)

        self._insert_into_parent_node(leaf_node, value)

    def _insert_into_parent_node(self, parent: BSTNode[T] | None, value: T) -> None:
        self._insert_node_into_parent_node(parent, BSTNode(value))

    def _insert_node_into_parent_node(self, parent: BSTNode[T] | None, node: BSTNode[T] | None) -> None:
        if parent is None or node is None:
            return

        comparison = self.comp(node.value, parent.value)
        if comparison < 0:
            parent.set_left(node)
        elif comparison > 0:
            parent.set_right(node)
        else:
            # Duplicate value, do not insert
            return

        self._increase_size()

    def _delete(self, value: T) -> None:
        if self.size() < 1000:
            self._delete_by_recursive(self.root, value)
        else:
            self._delete_by_loop(value)

    def _delete_by_recursive(self, node: BSTNode[T] | None, value: T) -> None:
        if node is None:
            return

        comparison = self.comp(value, node.value)
        if comparison < 0:
            self._delete_by_recursive(node.left, value)
        elif comparison > 0:
            self._delete_by_recursive(node.right, value)
        else:
            self._delete_node(node)

    def _delete_by_loop(self, value: T) -> None:
        current = self.root

        while current is not None:
            comparison = self.comp(value, current.value)
            if comparison < 0:
                current = current.left
            elif comparison > 0:
                current = current.right
            else:
                break

        if current is None:
            return

        self._delete_node(current)

    def _delete_node(self, node: BSTNode[T]):
        """
        The node is removed from the BST, and the tree is restructured accordingly.

        1. If the node has no left child, replace it with its right child.
        2. If the node has no right child, replace it with its left child.
        3. If the node has both children, find its successor (the smallest node in its right subtree),
        replace the node's value with the successor's value,
        and then delete the successor node (which will have at most one child).

        Args:
            node: The node to be deleted from the BST.

        """
        if node.left is None:
            self._transplant(node, node.right)
        elif node.right is None:
            self._transplant(node, node.left)
        else:
            next_node = self.successor(node)
            if next_node is not node.right:
                self._transplant(next_node, next_node.right)
                next_node.set_right(node.right)

            self._transplant(node, next_node)
            next_node.set_left(node.left)

        self._decrease_size()

    def _transplant(self, target: BSTNode[T] | None, replacement: BSTNode[T] | None) -> None:
        """
        target이 있던 자리를 replacement로 갈아끼운다 (CLRS TRANSPLANT).
        target 자신의 left/right는 건드리지 않고, target.parent 쪽에서 target을 가리키던 링크만 replacement로 바꾼다.
        """
        if target is None:
            return

        if target.is_root():
            self.root = replacement
            if replacement is not None:
                replacement.parent = None
        elif target.is_left_child():
            target.parent.set_left(replacement)
        else:
            target.parent.set_right(replacement)

    def _increase_size(self) -> None:
        self._size += 1

    def _decrease_size(self) -> None:
        self._size -= 1

    @staticmethod
    def find_min_node(node: BSTNode[T]) -> BSTNode[T]:
        while node.left is not None:
            node = node.left

        return node

    @staticmethod
    def find_max_node(node: BSTNode[T]) -> BSTNode[T]:
        while node.right is not None:
            node = node.right

        return node

    @classmethod
    def successor(cls, node: BSTNode[T]) -> BSTNode[T] | None:
        """

        Args:
            node: The node for which to find the successor in the BST.

        Returns: The successor node of the given node in the BST, or None if there is no successor.

        """
        if node.right is not None:
            return cls.find_min_node(node.right)

        # If the node has no right child, the successor is one of its ancestors.
        current, parent = node, node.parent
        while parent is not None and current is parent.right:
            current, parent = parent, parent.parent

        return parent

    @classmethod
    def predecessor(cls, node: BSTNode[T]) -> BSTNode[T] | None:
        """

        Args:
            node: The node for which to find the predecessor in the BST.

        Returns: The predecessor node of the given node in the BST, or None if there is no predecessor.

        """
        if node.left is not None:
            return cls.find_max_node(node.left)

        # If the node has no left child, the predecessor is one of its ancestors.
        current, parent = node, node.parent
        while parent is not None and current is parent.left:
            current, parent = parent, parent.parent

        return parent


if __name__ == "__main__":
    bst = BinarySearchTree([5, 3, 8, 1, 4, 7, 9, 2, 6])
    bst.print_tree()
    print(bst.inorder())
    print(bst.size())

    bst.add(10)
    bst.add(0)
    print(bst.inorder())

    bst.remove(3)
    bst.remove(9)
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

    people_bst.remove(Person('', 30))
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
