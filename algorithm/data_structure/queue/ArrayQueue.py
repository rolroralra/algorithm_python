from typing import TypeVar

from algorithm.data_structure.queue.Queue import Queue

T = TypeVar('T')

class ArrayQueue(Queue[T]):
    def __init__(self):
        self.items = []

    def enqueue(self, data: T) -> None:
        self.items.append(data)

    def dequeue(self) -> T:
        return self.items.pop(0)

    def peek(self) -> T:
        return self.items[0]

    def is_empty(self) -> bool:
        return self.size() == 0

    def size(self) -> int:
        return len(self.items)

    def to_list(self) -> list[T]:
        return self.items.copy()

