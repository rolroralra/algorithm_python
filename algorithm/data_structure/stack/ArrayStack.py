from typing import TypeVar
from algorithm.data_structure.stack.Stack import Stack

T = TypeVar('T')

class ArrayStack(Stack[T]):
    def __init__(self):
        self.items = []

    def is_empty(self) -> bool:
        return len(self.items) == 0

    def push(self, item: T):
        self.items.append(item)

    def pop(self) -> T:
        if self.is_empty():
            raise IndexError("pop from empty stack")

        return self.items.pop()

    def peek(self) -> T:
        if self.is_empty():
            raise IndexError("peek from empty stack")

        return self.items[-1]

    def size(self) -> int:
        return len(self.items)

    def to_list(self) -> list[T]:
        return self.items.copy()