import pytest

from algorithm.articulation.articulation_point import articulation_points


def undirected(edges: list[tuple[int, int]], vertex_count: int) -> list[list[int]]:
    adj_list = [[] for _ in range(vertex_count)]
    for a, b in edges:
        adj_list[a].append(b)
        adj_list[b].append(a)
    return adj_list


@pytest.mark.unit
class TestArticulationPoints:
    def test_triangle_has_no_articulation_points(self):
        adj_list = undirected([(0, 1), (1, 2), (2, 0)], 3)

        assert articulation_points(adj_list) == []

    def test_bridge_endpoint_is_an_articulation_point(self):
        # triangle 0-1-2 connected to 3 via a bridge, 3 connected to 4
        adj_list = undirected([(0, 1), (1, 2), (2, 0), (1, 3), (3, 4)], 5)

        assert sorted(articulation_points(adj_list)) == [1, 3]

    def test_simple_path_has_internal_nodes_as_articulation_points(self):
        adj_list = undirected([(0, 1), (1, 2), (2, 3)], 4)

        assert sorted(articulation_points(adj_list)) == [1, 2]

    def test_two_vertex_graph_has_no_articulation_points(self):
        adj_list = undirected([(0, 1)], 2)

        assert articulation_points(adj_list) == []

    def test_single_vertex_no_edges(self):
        assert articulation_points([[]]) == []

    def test_star_graph_center_is_the_only_articulation_point(self):
        adj_list = undirected([(0, 1), (0, 2), (0, 3)], 4)

        assert articulation_points(adj_list) == [0]

    def test_disconnected_components_evaluated_independently(self):
        adj_list = undirected([(0, 1), (1, 2), (3, 4)], 5)

        assert articulation_points(adj_list) == [1]
