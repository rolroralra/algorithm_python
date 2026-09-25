import pytest

from algorithm.data_structure.queue.ArrayQueue import ArrayQueue


@pytest.mark.unit
class TestArrayQueueBasics:
    def test_new_queue_is_empty(self):
        queue = ArrayQueue()
        assert queue.is_empty()
        assert queue.size() == 0
        assert queue.to_list() == []

    def test_dequeue_on_empty_queue_raises(self):
        queue = ArrayQueue()
        with pytest.raises(IndexError):
            queue.dequeue()

    def test_peek_on_empty_queue_raises(self):
        queue = ArrayQueue()
        with pytest.raises(IndexError):
            queue.peek()


@pytest.mark.unit
class TestArrayQueueEnqueueDequeue:
    def test_enqueue_preserves_all_items_in_order(self):
        queue = ArrayQueue()
        queue.enqueue(1)
        queue.enqueue(2)
        queue.enqueue(3)

        assert queue.to_list() == [1, 2, 3]
        assert queue.size() == 3

    def test_dequeue_returns_items_in_fifo_order(self):
        queue = ArrayQueue()
        for value in [1, 2, 3]:
            queue.enqueue(value)

        assert [queue.dequeue() for _ in range(3)] == [1, 2, 3]
        assert queue.is_empty()

    def test_peek_returns_front_item_without_removing_it(self):
        queue = ArrayQueue()
        queue.enqueue(1)
        queue.enqueue(2)

        assert queue.peek() == 1
        assert queue.peek() == 1
        assert queue.size() == 2

    def test_dequeue_updates_size(self):
        queue = ArrayQueue()
        queue.enqueue(1)
        queue.enqueue(2)
        queue.dequeue()

        assert queue.size() == 1
        assert queue.peek() == 2

    def test_queue_is_usable_after_emptying_and_refilling(self):
        queue = ArrayQueue()
        queue.enqueue(1)
        queue.dequeue()
        assert queue.is_empty()

        queue.enqueue(9)
        assert queue.to_list() == [9]
        assert queue.peek() == 9


@pytest.mark.unit
class TestArrayQueueToList:
    def test_to_list_returns_a_copy_not_a_reference(self):
        queue = ArrayQueue()
        queue.enqueue(1)
        queue.enqueue(2)

        snapshot = queue.to_list()
        snapshot.append(999)

        assert queue.to_list() == [1, 2]


@pytest.mark.unit
class TestArrayQueueStressSequence:
    def test_interleaved_enqueue_and_dequeue_keep_fifo_order(self):
        queue = ArrayQueue()
        reference = []

        for value in range(1, 6):
            queue.enqueue(value)
            reference.append(value)
        assert queue.to_list() == reference

        assert queue.dequeue() == reference.pop(0)
        assert queue.to_list() == reference

        queue.enqueue(10)
        reference.append(10)
        assert queue.to_list() == reference

        while reference:
            assert queue.dequeue() == reference.pop(0)

        assert queue.is_empty()
        assert queue.size() == 0
