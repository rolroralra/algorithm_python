import pytest

from algorithm.articulation.articulation_edge import articulation_edges


def undirected(edges: list[tuple[int, int]], vertex_count: int) -> list[list[int]]:
    adj_list = [[] for _ in range(vertex_count)]
    for a, b in edges:
        adj_list[a].append(b)
        adj_list[b].append(a)
    return adj_list


@pytest.mark.unit
class TestArticulationEdges:
    def test_triangle_has_no_bridges(self):
        adj_list = undirected([(0, 1), (1, 2), (2, 0)], 3)

        assert articulation_edges(adj_list) == []

    def test_bridges_connecting_a_cycle_to_pendant_vertices(self):
        adj_list = undirected([(0, 1), (1, 2), (2, 0), (1, 3), (3, 4)], 5)

        assert sorted(articulation_edges(adj_list)) == [(1, 3), (3, 4)]

    def test_every_edge_in_a_simple_path_is_a_bridge(self):
        adj_list = undirected([(0, 1), (1, 2), (2, 3)], 4)

        assert sorted(articulation_edges(adj_list)) == [(0, 1), (1, 2), (2, 3)]

    def test_star_graph_every_edge_is_a_bridge(self):
        adj_list = undirected([(0, 1), (0, 2), (0, 3)], 4)

        assert sorted(articulation_edges(adj_list)) == [(0, 1), (0, 2), (0, 3)]

    def test_disconnected_components_evaluated_independently(self):
        adj_list = undirected([(0, 1), (1, 2), (3, 4)], 5)

        assert sorted(articulation_edges(adj_list)) == [(0, 1), (1, 2), (3, 4)]

    def test_single_vertex_no_edges(self):
        assert articulation_edges([[]]) == []
