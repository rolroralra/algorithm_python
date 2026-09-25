import random

import pytest

from algorithm.data_structure.queue.CircularQueue import CircularQueue


@pytest.mark.unit
class TestCircularQueueBasics:
    def test_new_queue_is_empty(self):
        cq = CircularQueue(5)
        assert cq.is_empty()
        assert not cq.is_full()
        assert cq.peek() is None
        assert cq.dequeue() is None

    def test_enqueue_then_peek_does_not_dequeue(self):
        cq = CircularQueue(3)
        cq.enqueue(1)

        assert cq.peek() == 1
        assert cq.peek() == 1
        assert not cq.is_empty()

    def test_fifo_order(self):
        cq = CircularQueue(5)
        for value in [1, 2, 3, 4]:
            cq.enqueue(value)

        assert [cq.dequeue() for _ in range(4)] == [1, 2, 3, 4]

    def test_is_full_when_all_slots_are_used(self):
        # front stays fixed while filling from empty, so all `size` slots
        # are usable before (rear + 1) % size wraps onto front.
        cq = CircularQueue(5)
        for value in range(5):
            cq.enqueue(value)

        assert cq.is_full()

    def test_enqueue_on_full_queue_is_noop(self):
        cq = CircularQueue(3)
        cq.enqueue(1)
        cq.enqueue(2)
        cq.enqueue(3)
        assert cq.is_full()

        cq.enqueue(4)  # should be ignored, queue stays full with original data

        assert cq.dequeue() == 1
        assert cq.dequeue() == 2
        assert cq.dequeue() == 3
        assert cq.is_empty()

    def test_dequeue_on_empty_queue_returns_none_and_stays_empty(self):
        cq = CircularQueue(3)
        assert cq.dequeue() is None
        assert cq.is_empty()


@pytest.mark.unit
class TestCircularQueueFrontRearWraparound:
    def test_front_and_rear_reset_after_queue_becomes_empty(self):
        cq = CircularQueue(3)
        cq.enqueue(1)
        cq.enqueue(2)
        cq.dequeue()
        cq.dequeue()

        assert cq.is_empty()
        assert cq.front == -1
        assert cq.rear == -1

    def test_rear_wraps_around_after_dequeue_makes_room(self):
        cq = CircularQueue(5)
        for value in [1, 2, 3, 4, 5]:
            cq.enqueue(value)
        assert cq.is_full()  # rear sits at the last slot (index 4)

        assert cq.dequeue() == 1  # front moves to index 1, one slot freed
        assert not cq.is_full()

        cq.enqueue(6)  # rear wraps from index 4 back to index 0

        assert cq.dequeue() == 2
        assert cq.dequeue() == 3
        assert cq.dequeue() == 4
        assert cq.dequeue() == 5
        assert cq.dequeue() == 6
        assert cq.is_empty()

    def test_repeated_fill_and_drain_cycles_keep_pointers_consistent(self):
        cq = CircularQueue(4)

        for cycle in range(10):
            base = cycle * 3
            values = [base, base + 1, base + 2]
            for value in values:
                cq.enqueue(value)

            drained = [cq.dequeue() for _ in range(len(values))]
            assert drained == values
            assert cq.is_empty()
            assert cq.front == -1
            assert cq.rear == -1

    def test_partial_fill_drain_interleaving_matches_expected_fifo(self):
        cq = CircularQueue(4)
        pending = []  # mirrors current queue contents (FIFO order)

        # Interleave enqueue/dequeue enough times to wrap the ring buffer
        # multiple times over and cross-check against a plain list FIFO.
        counter = 0
        for _ in range(50):
            if cq.is_full() or (pending and counter % 2 == 0):
                assert cq.dequeue() == pending.pop(0)
            else:
                cq.enqueue(counter)
                pending.append(counter)
            counter += 1

        while not cq.is_empty():
            assert cq.dequeue() == pending.pop(0)

        assert not pending

    @pytest.mark.parametrize("seed", range(10))
    def test_matches_reference_deque_under_random_operations(self, seed):
        random.seed(seed)
        capacity = 5
        cq = CircularQueue(capacity)
        reference = []  # all `capacity` slots are usable, see is_full() semantics

        for _ in range(200):
            if random.random() < 0.5 and len(reference) < capacity:
                value = random.randint(0, 1000)
                cq.enqueue(value)
                reference.append(value)
            elif reference:
                assert cq.dequeue() == reference.pop(0)
            else:
                assert cq.dequeue() is None

            assert cq.is_empty() == (len(reference) == 0)
            assert cq.is_full() == (len(reference) == capacity)

        while reference:
            assert cq.dequeue() == reference.pop(0)
        assert cq.is_empty()
