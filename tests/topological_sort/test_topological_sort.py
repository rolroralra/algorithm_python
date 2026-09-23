import pytest

from algorithm.topological_sort.topological_sort import (
    topological_sort_by_dfs_recursive,
    topological_sort_by_indegree,
)

IMPLEMENTATIONS = {
    "dfs_recursive": topological_sort_by_dfs_recursive,
    "indegree": topological_sort_by_indegree,
}


def assert_valid_topological_order(adj_list: list[list[int]], order: list[int]) -> None:
    position = {node: index for index, node in enumerate(order)}
    for u, neighbors in enumerate(adj_list):
        for v in neighbors:
            assert position[u] < position[v]


@pytest.mark.unit
class TestTopologicalSortOnDag:
    @pytest.mark.parametrize("topo_sort", IMPLEMENTATIONS.values(), ids=IMPLEMENTATIONS.keys())
    def test_includes_every_vertex(self, topo_sort):
        adj_list = [[1, 2], [3], [3], []]

        order, has_cycle = topo_sort(adj_list)

        assert has_cycle is False
        assert sorted(order) == list(range(len(adj_list)))

    @pytest.mark.parametrize("topo_sort", IMPLEMENTATIONS.values(), ids=IMPLEMENTATIONS.keys())
    def test_respects_edge_ordering(self, topo_sort):
        adj_list = [[1, 2], [3], [3], []]

        order, _ = topo_sort(adj_list)

        assert_valid_topological_order(adj_list, order)

    @pytest.mark.parametrize("topo_sort", IMPLEMENTATIONS.values(), ids=IMPLEMENTATIONS.keys())
    def test_disconnected_dag(self, topo_sort):
        adj_list = [[1], [], [3], []]

        order, has_cycle = topo_sort(adj_list)

        assert has_cycle is False
        assert_valid_topological_order(adj_list, order)
        assert sorted(order) == list(range(len(adj_list)))

    @pytest.mark.parametrize("topo_sort", IMPLEMENTATIONS.values(), ids=IMPLEMENTATIONS.keys())
    def test_single_vertex_no_edges(self, topo_sort):
        order, has_cycle = topo_sort([[]])

        assert has_cycle is False
        assert order == [0]


@pytest.mark.unit
class TestTopologicalSortOnCyclicGraph:
    @pytest.mark.parametrize("topo_sort", IMPLEMENTATIONS.values(), ids=IMPLEMENTATIONS.keys())
    def test_detects_simple_cycle(self, topo_sort):
        adj_list = [[1], [2], [0]]

        _, has_cycle = topo_sort(adj_list)

        assert has_cycle is True

    @pytest.mark.parametrize("topo_sort", IMPLEMENTATIONS.values(), ids=IMPLEMENTATIONS.keys())
    def test_detects_cycle_within_larger_graph(self, topo_sort):
        adj_list = [[1], [2], [1], []]

        _, has_cycle = topo_sort(adj_list)

        assert has_cycle is True

    @pytest.mark.parametrize("topo_sort", IMPLEMENTATIONS.values(), ids=IMPLEMENTATIONS.keys())
    def test_self_loop_is_a_cycle(self, topo_sort):
        adj_list = [[0]]

        _, has_cycle = topo_sort(adj_list)

        assert has_cycle is True
