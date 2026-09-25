import pytest

from algorithm.data_structure.linked_list.LinkedList import LinkedList
from algorithm.data_structure.linked_list.SinglyLinkedList import SinglyLinkedList

REQUIRED_ABSTRACT_METHODS = {
    "is_empty",
    "append",
    "append_first",
    "peek_first",
    "peek_last",
    "pop_first",
    "pop_last",
    "to_list",
    "contains",
    "delete",
}


@pytest.mark.unit
class TestLinkedListAbc:
    def test_declares_expected_abstract_methods(self):
        assert LinkedList.__abstractmethods__ == frozenset(REQUIRED_ABSTRACT_METHODS)

    def test_cannot_instantiate_directly(self):
        with pytest.raises(TypeError):
            LinkedList()

    def test_incomplete_subclass_cannot_be_instantiated(self):
        class Incomplete(LinkedList):
            def is_empty(self) -> bool:
                return True

        with pytest.raises(TypeError):
            Incomplete()

    def test_subclass_implementing_every_method_can_be_instantiated(self):
        class Complete(LinkedList):
            def is_empty(self) -> bool:
                return True

            def append(self, data) -> None:
                pass

            def append_first(self, data) -> None:
                pass

            def peek_first(self):
                pass

            def peek_last(self):
                pass

            def pop_first(self):
                pass

            def pop_last(self):
                pass

            def to_list(self) -> list:
                return []

            def contains(self, key) -> bool:
                return False

            def delete(self, key) -> None:
                pass

        assert isinstance(Complete(), LinkedList)


@pytest.mark.unit
class TestSinglyLinkedListConformsToLinkedList:
    def test_is_a_linked_list_subclass(self):
        assert issubclass(SinglyLinkedList, LinkedList)

    def test_instance_is_a_linked_list(self):
        assert isinstance(SinglyLinkedList(), LinkedList)

    def test_can_be_used_polymorphically_through_the_interface(self):
        linked_list: LinkedList[int] = SinglyLinkedList([1, 2, 3])

        assert not linked_list.is_empty()
        assert linked_list.to_list() == [1, 2, 3]
        assert linked_list.contains(2)

        linked_list.append(4)
        linked_list.append_first(0)
        assert linked_list.to_list() == [0, 1, 2, 3, 4]
        assert linked_list.peek_first() == 0
        assert linked_list.peek_last() == 4

        linked_list.delete(2)
        assert linked_list.to_list() == [0, 1, 3, 4]
