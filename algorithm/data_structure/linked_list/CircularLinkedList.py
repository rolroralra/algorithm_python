from typing import TypeVar
from algorithm.data_structure.linked_list.DoublyLinkedList import \
    DoublyLinkedList

EMPTY_MESSAGE = "CircularLinkedList is empty"

T = TypeVar('T')

class CircularLinkedList(DoublyLinkedList[T]):
    def append(self, data) -> None:
        new_node = self.Node(data)

        if self.is_empty():
            new_node.prev = new_node
            new_node.next = new_node
            self.head = new_node
            self.tail = new_node
            return

        new_node.prev = self.tail
        new_node.next = self.head
        self.tail.next = new_node
        self.head.prev = new_node
        self.tail = new_node

    def append_first(self, data) -> None:
        new_node = self.Node(data)

        if self.is_empty():
            new_node.prev = new_node
            new_node.next = new_node
            self.head = new_node
            self.tail = new_node
            return

        new_node.next = self.head
        new_node.prev = self.tail
        self.head.prev = new_node
        self.tail.next = new_node
        self.head = new_node

    def pop_first(self) -> T:
        if self.is_empty():
            raise ValueError(EMPTY_MESSAGE)

        result = self.head.data

        if self.head is self.tail:
            self.head = None
            self.tail = None
            return result

        new_head = self.head.next
        new_head.prev = self.tail
        self.tail.next = new_head
        self.head = new_head

        return result

    def pop_last(self) -> T:
        if self.is_empty():
            raise ValueError(EMPTY_MESSAGE)

        result = self.tail.data

        if self.head is self.tail:
            self.head = None
            self.tail = None
            return result

        new_tail = self.tail.prev
        new_tail.next = self.head
        self.head.prev = new_tail
        self.tail = new_tail

        return result

    def contains(self, key: T) -> bool:
        return self._find_node(key) is not None

    def delete(self, key: T) -> None:
        node = self._find_node(key)

        if node is None:
            return

        if node is self.head and node is self.tail:
            self.head = None
            self.tail = None
            return

        node.prev.next = node.next
        node.next.prev = node.prev

        if node is self.head:
            self.head = node.next
        if node is self.tail:
            self.tail = node.prev

    def to_list(self) -> list[T]:
        if self.is_empty():
            return []

        nodes = []
        current_node = self.head
        while True:
            nodes.append(current_node.data)
            current_node = current_node.next
            if current_node is self.head:
                break

        return nodes

    def _find_node(self, key: T) -> DoublyLinkedList.Node | None:
        if self.is_empty():
            return None

        current_node = self.head
        while True:
            if current_node.data == key:
                return current_node

            current_node = current_node.next
            if current_node is self.head:
                return None
