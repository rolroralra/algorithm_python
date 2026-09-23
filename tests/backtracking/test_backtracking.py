import pytest

from algorithm.backtracking import backtracking as backtracking_module
from algorithm.backtracking.backtracking import backtracking


@pytest.mark.unit
class TestBacktracking:
    def test_unwinds_all_visit_marks_after_full_traversal(self):
        graph = [[1, 2], [0, 3], [0], [1]]
        is_visited = [False] * len(graph)

        backtracking(graph, is_visited, 0)

        assert is_visited == [False] * len(graph)

    def test_handles_cyclic_graph_without_infinite_recursion(self):
        graph = [[1], [2], [0]]
        is_visited = [False] * len(graph)

        backtracking(graph, is_visited, 0)

        assert is_visited == [False] * len(graph)

    def test_single_node_with_no_edges(self):
        is_visited = [False]

        backtracking([[]], is_visited, 0)

        assert is_visited == [False]

    def test_extra_args_are_forwarded_without_error(self):
        graph = [[1], [0]]
        is_visited = [False, False]

        backtracking(graph, is_visited, 0, "path", 42)

        assert is_visited == [False, False]

    def test_pruning_stops_traversal_before_visiting(self, monkeypatch):
        monkeypatch.setattr(backtracking_module, "prunning", lambda: True)
        graph = [[1, 2], [0], [0]]
        is_visited = [False] * len(graph)

        backtracking(graph, is_visited, 0)

        assert is_visited == [False] * len(graph)
