import pytest

from algorithm.data_structure.stack.ArrayStack import ArrayStack


@pytest.mark.unit
class TestArrayStackBasics:
    def test_new_stack_is_empty(self):
        stack = ArrayStack()
        assert stack.is_empty()
        assert stack.size() == 0
        assert stack.to_list() == []

    def test_pop_on_empty_stack_raises(self):
        stack = ArrayStack()
        with pytest.raises(IndexError):
            stack.pop()

    def test_peek_on_empty_stack_raises(self):
        stack = ArrayStack()
        with pytest.raises(IndexError):
            stack.peek()


@pytest.mark.unit
class TestArrayStackPushPop:
    def test_push_preserves_all_items_in_order(self):
        stack = ArrayStack()
        stack.push(1)
        stack.push(2)
        stack.push(3)

        assert stack.to_list() == [1, 2, 3]
        assert stack.size() == 3

    def test_pop_returns_items_in_lifo_order(self):
        stack = ArrayStack()
        for value in [1, 2, 3]:
            stack.push(value)

        assert [stack.pop() for _ in range(3)] == [3, 2, 1]
        assert stack.is_empty()

    def test_peek_returns_top_item_without_removing_it(self):
        stack = ArrayStack()
        stack.push(1)
        stack.push(2)

        assert stack.peek() == 2
        assert stack.peek() == 2
        assert stack.size() == 2

    def test_pop_updates_size(self):
        stack = ArrayStack()
        stack.push(1)
        stack.push(2)
        stack.pop()

        assert stack.size() == 1
        assert stack.peek() == 1

    def test_stack_is_usable_after_emptying_and_refilling(self):
        stack = ArrayStack()
        stack.push(1)
        stack.pop()
        assert stack.is_empty()

        stack.push(9)
        assert stack.to_list() == [9]
        assert stack.peek() == 9


@pytest.mark.unit
class TestArrayStackToList:
    def test_to_list_returns_a_copy_not_a_reference(self):
        stack = ArrayStack()
        stack.push(1)
        stack.push(2)

        snapshot = stack.to_list()
        snapshot.append(999)

        assert stack.to_list() == [1, 2]


@pytest.mark.unit
class TestArrayStackStressSequence:
    def test_interleaved_push_and_pop_keep_lifo_order(self):
        stack = ArrayStack()
        reference = []

        for value in range(1, 6):
            stack.push(value)
            reference.append(value)
        assert stack.to_list() == reference

        assert stack.pop() == reference.pop()
        assert stack.to_list() == reference

        stack.push(10)
        reference.append(10)
        assert stack.to_list() == reference

        while reference:
            assert stack.pop() == reference.pop()

        assert stack.is_empty()
        assert stack.size() == 0
