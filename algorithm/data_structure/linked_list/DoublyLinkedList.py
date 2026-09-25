from typing import TypeVar

from algorithm.data_structure.linked_list.LinkedList import LinkedList

EMPTY_MESSAGE = "DoublyLinkedList is empty"

T = TypeVar('T')

class DoublyLinkedList(LinkedList[T]):
    class Node:
        def __init__(self, data):
            self.data = data
            self.prev = None
            self.next = None

    def __init__(self):
        self.head = None
        self.tail = None

    def is_empty(self) -> bool:
        return self.head is None or self.tail is None

    def append(self, data) -> None:
        new_node = self.Node(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
            return

        self.tail.next = new_node
        new_node.prev = self.tail
        self.tail = new_node

    def append_first(self, data) -> None:
        new_node = self.Node(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
            return

        new_node.next = self.head
        self.head.prev = new_node
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

        if self.head is self.tail:
            self.head = None
            self.tail = None
            return result

        self.head.next.prev = None
        self.head = self.head.next

        return result

    def pop_last(self) -> T:
        if self.is_empty():
            raise ValueError(EMPTY_MESSAGE)

        result = self.tail.data

        if self.head is self.tail:
            self.head = None
            self.tail = None
            return result

        self.tail.prev.next = None
        self.tail = self.tail.prev
        return result

    def contains(self, key: T) -> bool:
        current_node = self.head
        while current_node:
            if current_node.data == key:
                return True

            current_node = current_node.next

        return False

    def delete(self, key: T) -> None:
        node = self._find_node(key)

        if node is None:
            return

        if node.prev is not None:
            node.prev.next = node.next
        if node.next is not None:
            node.next.prev = node.prev

        if node is self.head:
            self.head = node.next
        if node is self.tail:
            self.tail = node.prev

    def to_list(self) -> list[T]:
        nodes = []
        current_node = self.head
        while current_node:
            nodes.append(current_node.data)
            current_node = current_node.next

        return nodes

    def _find_node(self, key: T) -> Node | None:
        current_node = self.head

        while current_node and current_node.data != key:
            current_node = current_node.next

        return current_node


