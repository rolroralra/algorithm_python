import pytest

from algorithm.data_structure.linked_list.CircularLinkedList import CircularLinkedList
from algorithm.data_structure.linked_list.DoublyLinkedList import DoublyLinkedList
from algorithm.data_structure.linked_list.SinglyLinkedList import SinglyLinkedList

LIST_IMPLEMENTATIONS = [SinglyLinkedList, DoublyLinkedList, CircularLinkedList]
IMPLEMENTATION_IDS = ["singly", "doubly", "circular"]


@pytest.fixture(params=LIST_IMPLEMENTATIONS, ids=IMPLEMENTATION_IDS)
def list_cls(request):
    return request.param


def _build(list_cls, values: list):
    instance = list_cls()
    for value in values:
        instance.append(value)
    return instance


@pytest.mark.unit
class TestLinkedListBasics:
    def test_new_list_is_empty(self, list_cls):
        ll = list_cls()
        assert ll.is_empty()
        assert ll.head is None
        assert ll.tail is None
        assert ll.to_list() == []

    def test_build_from_values_appends_in_order(self, list_cls):
        ll = _build(list_cls, [1, 2, 3])
        assert not ll.is_empty()
        assert ll.to_list() == [1, 2, 3]
        assert ll.peek_first() == 1
        assert ll.peek_last() == 3

    def test_peek_first_and_last_on_empty_list_raise(self, list_cls):
        ll = list_cls()
        with pytest.raises(ValueError):
            ll.peek_first()
        with pytest.raises(ValueError):
            ll.peek_last()

    def test_pop_first_on_empty_list_raises(self, list_cls):
        ll = list_cls()
        with pytest.raises(ValueError):
            ll.pop_first()


@pytest.mark.unit
class TestLinkedListAppend:
    def test_append_preserves_all_nodes_in_order(self, list_cls):
        ll = list_cls()
        ll.append(1)
        ll.append(2)
        ll.append(3)

        assert ll.to_list() == [1, 2, 3]
        assert ll.tail.data == 3
        assert ll.peek_last() == 3

    def test_append_updates_tail_reference_each_time(self, list_cls):
        ll = list_cls()
        ll.append(1)
        first_tail = ll.tail
        ll.append(2)

        assert ll.tail is not first_tail
        assert ll.tail.data == 2

    def test_append_after_emptying_list_starts_fresh(self, list_cls):
        ll = _build(list_cls, [1])
        ll.pop_first()
        assert ll.is_empty()

        ll.append(9)
        assert ll.to_list() == [9]
        assert ll.head is ll.tail

    def test_append_first_prepends_in_reverse_order(self, list_cls):
        ll = list_cls()
        ll.append_first(3)
        ll.append_first(2)
        ll.append_first(1)

        assert ll.to_list() == [1, 2, 3]
        assert ll.peek_first() == 1
        assert ll.peek_last() == 3

    def test_mixed_append_and_append_first(self, list_cls):
        ll = list_cls()
        ll.append(2)
        ll.append_first(1)
        ll.append(3)

        assert ll.to_list() == [1, 2, 3]
        assert ll.peek_last() == 3


@pytest.mark.unit
class TestLinkedListPopFirst:
    def test_pop_first_returns_and_removes_head(self, list_cls):
        ll = _build(list_cls, [1, 2, 3])
        assert ll.pop_first() == 1
        assert ll.to_list() == [2, 3]
        assert ll.peek_first() == 2

    def test_pop_first_last_element_empties_list_and_clears_tail(self, list_cls):
        ll = _build(list_cls, [1])
        assert ll.pop_first() == 1
        assert ll.is_empty()
        assert ll.head is None
        assert ll.tail is None

    def test_list_is_usable_after_pop_first_empties_and_refills(self, list_cls):
        ll = _build(list_cls, [1])
        ll.pop_first()
        ll.append(10)
        ll.append(20)

        assert ll.to_list() == [10, 20]
        assert ll.peek_last() == 20


@pytest.mark.unit
class TestLinkedListPopLast:
    def test_pop_last_returns_and_removes_tail(self, list_cls):
        ll = _build(list_cls, [1, 2, 3])
        assert ll.pop_last() == 3
        assert ll.to_list() == [1, 2]
        assert ll.peek_last() == 2

    def test_pop_last_single_element_empties_list_and_clears_head(self, list_cls):
        ll = _build(list_cls, [1])
        assert ll.pop_last() == 1
        assert ll.is_empty()
        assert ll.head is None
        assert ll.tail is None

    def test_pop_last_on_empty_list_raises(self, list_cls):
        ll = list_cls()
        with pytest.raises(ValueError):
            ll.pop_last()

    def test_repeated_pop_last_drains_list_in_reverse_order(self, list_cls):
        ll = _build(list_cls, [1, 2, 3, 4])
        assert [ll.pop_last() for _ in range(4)] == [4, 3, 2, 1]
        assert ll.is_empty()


@pytest.mark.unit
class TestLinkedListDelete:
    def test_delete_head_key(self, list_cls):
        ll = _build(list_cls, [1, 2, 3])
        ll.delete(1)
        assert ll.to_list() == [2, 3]

    def test_delete_middle_key(self, list_cls):
        ll = _build(list_cls, [1, 2, 3])
        ll.delete(2)
        assert ll.to_list() == [1, 3]

    def test_delete_tail_key_updates_tail_reference(self, list_cls):
        # Regression test: delete() must not leave self.tail pointing at the
        # unlinked node when the tail itself is removed, which would corrupt
        # any subsequent append()/peek_last()/pop_last() call.
        ll = _build(list_cls, [1, 2, 3])
        ll.delete(3)

        assert ll.to_list() == [1, 2]
        assert ll.tail.data == 2
        assert ll.peek_last() == 2

    def test_delete_tail_key_then_append_stays_consistent(self, list_cls):
        ll = _build(list_cls, [1, 2, 3])
        ll.delete(3)
        ll.append(4)

        assert ll.to_list() == [1, 2, 4]
        assert ll.peek_last() == 4

    def test_delete_only_element_empties_list(self, list_cls):
        ll = _build(list_cls, [1])
        ll.delete(1)

        assert ll.is_empty()
        assert ll.head is None
        assert ll.tail is None

    def test_delete_missing_key_is_noop(self, list_cls):
        ll = _build(list_cls, [1, 2, 3])
        ll.delete(999)
        assert ll.to_list() == [1, 2, 3]

    def test_delete_on_empty_list_is_noop(self, list_cls):
        ll = list_cls()
        ll.delete(1)
        assert ll.is_empty()

    def test_delete_first_matching_key_only(self, list_cls):
        ll = _build(list_cls, [1, 2, 2, 3])
        ll.delete(2)
        assert ll.to_list() == [1, 2, 3]


@pytest.mark.unit
class TestLinkedListContains:
    def test_contains_true_for_present_key(self, list_cls):
        ll = _build(list_cls, [1, 2, 3])
        assert ll.contains(2)

    def test_contains_false_for_missing_key(self, list_cls):
        ll = _build(list_cls, [1, 2, 3])
        assert not ll.contains(99)

    def test_contains_false_on_empty_list(self, list_cls):
        ll = list_cls()
        assert not ll.contains(1)


@pytest.mark.unit
class TestLinkedListStressSequence:
    def test_interleaved_operations_keep_head_tail_consistent(self, list_cls):
        ll = list_cls()
        reference = []

        for value in range(1, 6):
            ll.append(value)
            reference.append(value)
        assert ll.to_list() == reference

        ll.delete(3)
        reference.remove(3)
        assert ll.to_list() == reference
        assert ll.tail.data == reference[-1]

        ll.pop_last()
        reference.pop()
        assert ll.to_list() == reference
        assert ll.tail.data == reference[-1]

        ll.append_first(0)
        reference.insert(0, 0)
        assert ll.to_list() == reference

        ll.pop_first()
        reference.pop(0)
        assert ll.to_list() == reference

        while reference:
            ll.pop_last()
            reference.pop()

        assert ll.is_empty()
        assert ll.head is None
        assert ll.tail is None

        ll.append("fresh")
        assert ll.to_list() == ["fresh"]
        assert ll.peek_first() == ll.peek_last() == "fresh"


# --- Implementation-specific behavior not covered by the shared LinkedList interface ---


@pytest.mark.unit
class TestSinglyLinkedListExtras:
    def test_init_from_list_appends_in_order(self):
        sll = SinglyLinkedList([1, 2, 3])
        assert sll.to_list() == [1, 2, 3]
        assert sll.peek_first() == 1
        assert sll.peek_last() == 3

    def test_delete_first_removes_head_without_return_value(self):
        sll = SinglyLinkedList([1, 2, 3])
        sll.delete_first()
        assert sll.to_list() == [2, 3]

    def test_delete_first_on_single_element_list_clears_tail(self):
        sll = SinglyLinkedList([1])
        sll.delete_first()
        assert sll.is_empty()
        assert sll.head is None
        assert sll.tail is None

    def test_delete_first_on_empty_list_raises(self):
        sll = SinglyLinkedList()
        with pytest.raises(ValueError):
            sll.delete_first()
        assert sll.is_empty()

    def test_delete_last_removes_tail(self):
        sll = SinglyLinkedList([1, 2, 3])
        sll.delete_last()

        assert sll.to_list() == [1, 2]
        assert sll.peek_last() == 2
        assert sll.tail.data == 2

    def test_delete_last_on_single_element_list_empties_it(self):
        sll = SinglyLinkedList([42])
        sll.delete_last()

        assert sll.is_empty()
        assert sll.head is None
        assert sll.tail is None

    def test_delete_last_on_empty_list_raises(self):
        sll = SinglyLinkedList()
        with pytest.raises(ValueError):
            sll.delete_last()
        assert sll.is_empty()

    def test_repeated_delete_last_drains_list_in_reverse_order(self):
        sll = SinglyLinkedList([1, 2, 3, 4])
        drained = []
        while not sll.is_empty():
            drained.append(sll.peek_last())
            sll.delete_last()

        assert drained == [4, 3, 2, 1]


@pytest.mark.unit
class TestDoublyLinkedListExtras:
    def test_append_links_prev_pointer_to_previous_tail(self):
        dll = DoublyLinkedList()
        dll.append(1)
        first_tail = dll.tail
        dll.append(2)

        assert dll.tail.prev is first_tail

    def test_pop_first_clears_new_heads_prev_pointer(self):
        dll = _build(DoublyLinkedList, [1, 2, 3])
        dll.pop_first()
        assert dll.head.prev is None

    def test_delete_middle_key_relinks_next_nodes_prev_pointer(self):
        # Regression test: delete() must update node.next.prev, otherwise the
        # node following the deleted one keeps pointing at a detached node,
        # which corrupts pop_last()'s backward traversal.
        dll = _build(DoublyLinkedList, [1, 2, 3])
        dll.delete(2)

        assert dll.to_list() == [1, 3]
        third_node = dll.tail
        assert third_node.prev is dll.head


@pytest.mark.unit
class TestCircularLinkedListExtras:
    def test_single_element_node_points_to_itself(self):
        cll = _build(CircularLinkedList, [1])
        assert cll.head.next is cll.head
        assert cll.head.prev is cll.head

    def test_tail_wraps_around_to_head(self):
        cll = _build(CircularLinkedList, [1, 2, 3])
        assert cll.tail.next is cll.head
        assert cll.head.prev is cll.tail

    def test_wrap_around_holds_after_append_first(self):
        cll = _build(CircularLinkedList, [2, 3])
        cll.append_first(1)

        assert cll.to_list() == [1, 2, 3]
        assert cll.tail.next is cll.head
        assert cll.head.prev is cll.tail

    def test_wrap_around_holds_after_pop_first(self):
        cll = _build(CircularLinkedList, [1, 2, 3])
        cll.pop_first()

        assert cll.to_list() == [2, 3]
        assert cll.tail.next is cll.head
        assert cll.head.prev is cll.tail

    def test_wrap_around_holds_after_pop_last(self):
        cll = _build(CircularLinkedList, [1, 2, 3])
        cll.pop_last()

        assert cll.to_list() == [1, 2]
        assert cll.tail.next is cll.head
        assert cll.head.prev is cll.tail

    def test_wrap_around_holds_after_delete_middle_key(self):
        cll = _build(CircularLinkedList, [1, 2, 3])
        cll.delete(2)

        assert cll.to_list() == [1, 3]
        assert cll.tail.next is cll.head
        assert cll.head.prev is cll.tail

    def test_to_list_does_not_loop_forever_on_full_traversal(self):
        # Regression guard: to_list()/contains()/_find_node() must stop when
        # they wrap back to head instead of relying on a None sentinel, since
        # next/prev never become None in a circular list.
        cll = _build(CircularLinkedList, [1, 2, 3, 4, 5])
        assert cll.to_list() == [1, 2, 3, 4, 5]
        assert cll.contains(5)
        assert not cll.contains(999)
