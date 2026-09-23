import pytest

from algorithm.dfs.dfs import dfs


@pytest.mark.unit
class TestDfs:
    @pytest.mark.parametrize("recursive", [False, True], ids=["iterative", "recursive"])
    def test_visits_every_reachable_node(self, recursive):
        graph = [[1, 2], [0, 3], [0, 4], [1], [2]]
        is_visited = [False] * len(graph)

        dfs(graph, is_visited, 0, recursive)

        assert is_visited == [True] * len(graph)

    @pytest.mark.parametrize("recursive", [False, True], ids=["iterative", "recursive"])
    def test_does_not_visit_unreachable_nodes(self, recursive):
        graph = [[1], [0], [3], [2]]
        is_visited = [False] * len(graph)

        dfs(graph, is_visited, 0, recursive)

        assert is_visited == [True, True, False, False]

    @pytest.mark.parametrize("recursive", [False, True], ids=["iterative", "recursive"])
    def test_single_node_with_no_edges(self, recursive):
        graph = [[]]
        is_visited = [False]

        dfs(graph, is_visited, 0, recursive)

        assert is_visited == [True]

    @pytest.mark.parametrize("recursive", [False, True], ids=["iterative", "recursive"])
    def test_handles_cyclic_graph_without_infinite_loop(self, recursive):
        graph = [[1], [2], [0]]
        is_visited = [False] * len(graph)

        dfs(graph, is_visited, 0, recursive)

        assert is_visited == [True, True, True]

    @pytest.mark.parametrize("recursive", [False, True], ids=["iterative", "recursive"])
    def test_starts_from_arbitrary_start_index(self, recursive):
        graph = [[1], [0, 2], [1]]
        is_visited = [False] * len(graph)

        dfs(graph, is_visited, 2, recursive)

        assert is_visited == [True, True, True]
