from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar('T')

class Stack(ABC, Generic[T]):
    @abstractmethod
    def peek(self) -> T:
        raise NotImplementedError

    @abstractmethod
    def pop(self) -> T:
        raise NotImplementedError

    @abstractmethod
    def push(self, item: T) -> None:
        raise NotImplementedError

    @abstractmethod
    def is_empty(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def size(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def to_list(self) -> list[T]:
        raise NotImplementedError

    def display(self) -> None:
        if self.is_empty():
            print('Stack is empty')
            return

        print(self.to_list())