from typing import TypeVar
from algorithm.data_structure.linked_list.LinkedList import LinkedList

EMPTY_MESSAGE = "SinglyLinkedList is empty"

T = TypeVar('T')

class SinglyLinkedList(LinkedList[T]):
    class Node:
        def __init__(self, data: T):
            self.data = data
            self.next = None

    def __init__(self, init_data: list[T]|None = None):
        self.head = None
        self.tail = None

        if init_data is not None:
            for data in init_data:
                self.append(data)

    def is_empty(self) -> bool:
        return self.head is None or self.tail is None

    def append(self, data):
        new_node = self.Node(data)

        if self.is_empty():
            self.head = new_node
            self.tail = new_node
            return

        self.tail.next = new_node
        self.tail = new_node

    def append_first(self, data):
        new_node = self.Node(data)

        if self.is_empty():
            self.head = new_node
            self.tail = new_node
            return

        new_node.next = self.head
        self.head = new_node

    def peek_first(self) -> T:
        if self.is_empty():
            raise ValueError(EMPTY_MESSAGE)

        return self.head.data

    def peek_last(self) -> T:
        if self.is_empty():
            raise ValueError(EMPTY_MESSAGE)

        return self.tail.data

    def pop_first(self) -> T:
        if self.is_empty():
            raise ValueError(EMPTY_MESSAGE)

        result = self.head.data
        self.head = self.head.next

        if self.head is None:
            self.tail = None

        return result

    def pop_last(self) -> T:
        if self.is_empty():
            raise ValueError(EMPTY_MESSAGE)

        result = self.tail.data

        if self.head is self.tail:
            self.head = None
            self.tail = None
            return result

        new_tail_node = self.head
        while new_tail_node.next is not self.tail:
            new_tail_node = new_tail_node.next

        self.tail = new_tail_node
        self.tail.next = None

        return result

    def delete_first(self) -> None:
        self.pop_first()

    def delete_last(self) -> None:
        self.pop_last()

    def delete(self, key: T) -> None:
        current_node, prev_node = self._find_node(key)

        if current_node is None:
            return

        if prev_node is not None:
            prev_node.next = current_node.next

        if current_node is self.head:
            self.head = current_node.next

        if current_node is self.tail:
            self.tail = prev_node

    def contains(self, key: T) -> bool:
        current_node = self.head
        while current_node is not None:
            if current_node.data == key:
                return True

            current_node = current_node.next
        return False

    def to_list(self) -> list[T]:
        nodes = []
        current_node = self.head
        while current_node is not None:
            nodes.append(current_node.data)
            current_node = current_node.next
        return nodes

    def _find_node(self, key: T) -> tuple[Node|None, Node|None]:
        current_node = self.head
        prev_node = None

        while current_node and current_node.data != key:
            prev_node = current_node
            current_node = current_node.next

        return current_node, prev_node