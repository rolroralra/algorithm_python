import pytest

from algorithm.mst.minimal_spanning_tree import (
    MinimalSpanningTreeAlgorithm,
    minimal_spanning_tree,
    mst_kruskal_algorithm,
    mst_prim_algorithm,
)


@pytest.mark.unit
class TestKruskalAlgorithm:
    def test_computes_minimum_total_length(self):
        edges = [(0, 1, 1), (1, 2, 2), (0, 2, 3), (2, 3, 4), (1, 3, 5)]

        length, selected_edges = mst_kruskal_algorithm(edges, vertex_size=4)

        assert length == 7
        assert len(selected_edges) == 3

    def test_infers_vertex_size_when_not_given(self):
        edges = [(0, 1, 1), (1, 2, 2), (0, 2, 3)]

        length, selected_edges = mst_kruskal_algorithm(edges)

        assert length == 3
        assert len(selected_edges) == 2

    def test_single_edge_graph(self):
        length, selected_edges = mst_kruskal_algorithm([(0, 1, 5)], vertex_size=2)

        assert length == 5
        assert selected_edges == [(0, 1, 5)]

    def test_selected_edges_form_a_spanning_tree(self):
        edges = [(0, 1, 4), (0, 2, 1), (1, 2, 2), (1, 3, 5), (2, 3, 8), (2, 4, 10), (3, 4, 2)]

        _, selected_edges = mst_kruskal_algorithm(edges, vertex_size=5)

        assert len(selected_edges) == 4
        touched_vertices = {v for a, b, _ in selected_edges for v in (a, b)}
        assert touched_vertices == {0, 1, 2, 3, 4}


@pytest.mark.unit
class TestPrimAlgorithm:
    def test_computes_minimum_total_length(self):
        adj_list = [
            [(1, 1), (2, 3)],
            [(0, 1), (2, 2), (3, 5)],
            [(0, 3), (1, 2), (3, 4)],
            [(1, 5), (2, 4)],
        ]

        length, selected_edges = mst_prim_algorithm(adj_list)

        assert length == 7
        assert len(selected_edges) == 3

    def test_single_vertex_graph(self):
        length, selected_edges = mst_prim_algorithm([[]])

        assert length == 0
        assert selected_edges == []

    def test_matches_kruskal_on_same_graph(self):
        edges = [(0, 1, 4), (0, 2, 1), (1, 2, 2), (1, 3, 5), (2, 3, 8), (2, 4, 10), (3, 4, 2)]
        adj_list = [[] for _ in range(5)]
        for a, b, length in edges:
            adj_list[a].append((b, length))
            adj_list[b].append((a, length))

        kruskal_length, _ = mst_kruskal_algorithm(list(edges), vertex_size=5)
        prim_length, _ = mst_prim_algorithm(adj_list)

        assert kruskal_length == prim_length


@pytest.mark.unit
class TestMinimalSpanningTreeDispatcher:
    def test_dispatches_to_kruskal(self):
        edges = [(0, 1, 1), (1, 2, 2), (0, 2, 3)]

        length, _ = minimal_spanning_tree(edges, MinimalSpanningTreeAlgorithm.KRUSKAL_ALGORITHM)

        assert length == 3

    def test_dispatches_to_prim(self):
        adj_list = [[(1, 1), (2, 3)], [(0, 1), (2, 2)], [(0, 3), (1, 2)]]

        length, _ = minimal_spanning_tree(adj_list, MinimalSpanningTreeAlgorithm.PRIM_ALGORITHM)

        assert length == 3
