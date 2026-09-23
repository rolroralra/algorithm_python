import pytest

from algorithm.bfs.bfs import bfs


# bfs() keeps its visited-state internal and returns None, so these tests can
# only confirm it traverses without error for each graph shape.
@pytest.mark.unit
class TestBfs:
    def test_connected_graph_runs_without_error(self):
        graph = [[1, 2], [0, 3], [0, 4], [1], [2]]
        assert bfs(graph, 0) is None

    def test_disconnected_graph_runs_without_error(self):
        graph = [[1], [0], [3], [2]]
        assert bfs(graph, 0) is None

    def test_single_node_with_no_edges(self):
        assert bfs([[]], 0) is None

    def test_cyclic_graph_terminates(self):
        graph = [[1], [2], [0]]
        assert bfs(graph, 0) is None

    def test_starts_from_arbitrary_start_index(self):
        graph = [[1], [0, 2], [1]]
        assert bfs(graph, 2) is None

    def test_invalid_start_index_raises(self):
        with pytest.raises(IndexError):
            bfs([[0]], 5)
