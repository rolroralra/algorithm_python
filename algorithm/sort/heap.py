class Heap:
    def __init__(self, input_array=None, comp=lambda a, b: a > b):
        if input_array is None:
            input_array = []

        self.array = input_array
        self.comp = comp

        if self.array:
            self._heapify_bottom_up()

    def _heapify_bottom_up(self):
        for i in range((len(self.array) - 1) // 2, -1, -1):
            self._sift_down(i)

    def _heapify_top_down(self):
        for i in range(1, len(self.array)):
            self._sift_up(i)

    def add(self, val):
        self.array.append(val)
        self._sift_up(len(self.array) - 1)

    def pop(self):
        if len(self.array) == 0:
            return None
        if len(self.array) == 1:
            return self.array.pop()
        max_val = self.array[0]
        self.array[0] = self.array.pop()
        self._sift_down_recursive(0)
        return max_val

    def peek(self):
        return self.array[0] if self.array else None

    def _sift_up(self, index):
        self._sift_up_loop(index)

    def _sift_up_loop(self, index):
        while index > 0:
            parent_index = (index - 1) // 2
            if not self.comp(self.array[index], self.array[parent_index]):
                break

            self.array[index], self.array[parent_index] = self.array[parent_index], self.array[index]
            index = parent_index

    def _sift_up_recursive(self, index):
        parent_index = self.parent_index(index)
        if index > 0 and self.comp(self.array[index], self.array[parent_index]):
            self.array[index], self.array[parent_index] = self.array[parent_index], self.array[index]
            self._sift_up(parent_index)

    def _sift_down(self, index):
        self._sift_down_loop(index)

    def _sift_down_loop(self, index):
        left_child_index, right_child_index = self.child_indices(index)

        while left_child_index < self.size():
            target_index = index
            if left_child_index < self.size() and self.comp(self.array[left_child_index], self.array[target_index]):
                target_index = left_child_index
            if right_child_index < self.size() and self.comp(self.array[right_child_index], self.array[target_index]):
                target_index = right_child_index

            if target_index == index:
                break

            self.array[index], self.array[target_index] = self.array[target_index], self.array[index]
            index = target_index
            left_child_index, right_child_index = self.child_indices(index)

    def _sift_down_recursive(self, index):
        target_index = index
        left_child_index, right_child_index = self.child_indices(index)

        if left_child_index < self.size() and self.comp(self.array[left_child_index], self.array[target_index]):
            target_index = left_child_index
        if right_child_index < self.size() and self.comp(self.array[right_child_index], self.array[target_index]):
            target_index = right_child_index

        if target_index != index:
            self.array[index], self.array[target_index] = self.array[target_index], self.array[index]
            self._sift_down_recursive(target_index)

    def get_max(self):
        return self.array[0] if self.array else None

    def size(self):
        return len(self.array)

    def is_empty(self):
        return len(self.array) == 0

    def is_valid_index(self, index):
        return 0 <= index < len(self.array)

    def child_indices(self, index) -> tuple[int, int]:
        return self.left_child_index(index), self.right_child_index(index)

    def _compare_by_index(self, index1, index2):
        return (self.is_valid_index(index1) and self.is_valid_index(index2)
                and self.comp(self.array[index1], self.array[index2]))

    @staticmethod
    def parent_index(index):
        return (index - 1) // 2

    @staticmethod
    def left_child_index(index):
        return 2 * index + 1

    @staticmethod
    def right_child_index(index):
        return 2 * index + 2

    @staticmethod
    def heap_sort(input_array, comp=lambda a, b: a > b):
        heap_instance = Heap(input_array, comp)
        sorted_array = []
        while not heap_instance.is_empty():
            sorted_array.append(heap_instance.pop())
        return sorted_array

if __name__ == "__main__":
    heap = Heap()
    heap.add(3)
    heap.add(1)
    heap.add(4)
    heap.add(1)
    heap.add(5)
    heap.add(9)
    heap.add(2)
    heap.add(6)
    heap.add(5)
    heap.add(3)
    heap.add(5)

    while not heap.is_empty():
        print(heap.pop(), end=' ')
    print()

    heap = Heap([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5])
    while not heap.is_empty():
        print(heap.pop(), end=' ')
    print()

    array = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    sorted_array = Heap.heap_sort(array, lambda a, b: a < b)
    print(sorted_array)
