from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar('T')


class LinkedList(ABC, Generic[T]):
    @abstractmethod
    def is_empty(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def append(self, data: T) -> None:
        raise NotImplementedError

    @abstractmethod
    def append_first(self, data: T) -> None:
        raise NotImplementedError

    @abstractmethod
    def peek_first(self) -> T:
        raise NotImplementedError

    @abstractmethod
    def peek_last(self) -> T:
        raise NotImplementedError

    @abstractmethod
    def pop_first(self) -> T:
        raise NotImplementedError

    @abstractmethod
    def pop_last(self) -> T:
        raise NotImplementedError

    @abstractmethod
    def contains(self, key: T) -> bool:
        raise NotImplementedError

    @abstractmethod
    def delete(self, key: T) -> None:
        raise NotImplementedError

    @abstractmethod
    def to_list(self) -> list[T]:
        raise NotImplementedError

    def display(self) -> None:
        if self.is_empty():
            print('LinkedList is empty')
            return

        print(self.to_list())


