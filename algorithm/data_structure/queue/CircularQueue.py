from typing import TypeVar

from algorithm.data_structure.queue.Queue import Queue

T = TypeVar('T')

class CircularQueue(Queue[T]):
    def __init__(self, size):
        self.size = size
        self.queue = [None] * size
        self._init_front()
        self._init_rear()
        assert self.is_empty()

    def is_full(self) -> bool:
        return (self.rear + 1) % self.size == self.front

    def is_empty(self) -> bool:
        return self.front == -1

    def size(self) -> int:
        return self.size

    def enqueue(self, data) -> None:
        if self.is_full():
            print("Queue is full")
            return

        # If the queue is empty, set front to 0
        if self.is_empty():
            self.front = 0

        # Move rear to the next position in a circular manner
        self.rear = (self.rear + 1) % self.size
        self.queue[self.rear] = data

    def dequeue(self) -> T:
        if self.is_empty():
            print("Queue is empty")
            return None

        # Retrieve the data at the front of the queue
        data = self.queue[self.front]

        # If the queue has only one element, reset front and rear to -1
        if self.front == self.rear:
            self._init_front()
            self._init_rear()
            assert self.is_empty()
        else:
            # Move front to the next position in a circular manner
            self.front = (self.front + 1) % self.size
        return data

    def peek(self) -> T:
        if self.is_empty():
            print("Queue is empty")
            return None

        # Return the data at the front of the queue without removing it
        return self.queue[self.front]

    def to_list(self) -> list[T]:
        pass

    # Private methods to initialize front
    def _init_front(self):
        self.front = -1

    # Private method to initialize rear
    def _init_rear(self):
        self.rear = -1

if __name__ == '__main__':
    cq = CircularQueue(5)
    cq.enqueue(1)
    cq.enqueue(2)
    cq.enqueue(3)
    cq.enqueue(4)
    cq.enqueue(5)
    cq.display()        # Output: 1 2 3 4 5
    print(cq.dequeue()) # Output: 1
    print(cq.peek())    # Output: 2
    cq.display()        # Output: 2 3 4 5

    cq.enqueue(6)
    cq.dequeue()
    cq.display()        # Output: 3 4 5 6
    cq.enqueue(7)
    cq.display()        # Output: 3 4 5 6 7
    cq.enqueue(8)       # Output: Queue is full
    cq.dequeue()
    cq.display()        # Output: 4 5 6 7
    cq.dequeue()
    cq.display()        # Output: 5 6 7
    cq.enqueue(8)
    cq.enqueue(9)
    cq.display()        # Output: 5 6 7 8 9
    cq.dequeue()
    cq.dequeue()
    cq.dequeue()
    cq.dequeue()
    cq.dequeue()
    cq.dequeue()        # Output: Queue is empty
    cq.display()        # Output: Queue is empty
