import sys

import pytest

from algorithm.floyd_warshall.floyd_warshall import floyd_warshall, shortest_path

INF = sys.maxsize


def build_matrix(n: int, edges: list[tuple[int, int, int]]) -> list[list[int]]:
    matrix = [[INF] * n for _ in range(n)]
    for a, b, weight in edges:
        matrix[a][b] = weight
    return matrix


@pytest.mark.unit
class TestFloydWarshall:
    def test_self_distance_is_zero(self):
        matrix = build_matrix(3, [(0, 1, 1), (1, 2, 1)])

        distance, _ = floyd_warshall(matrix)

        assert distance[0][0] == 0
        assert distance[1][1] == 0
        assert distance[2][2] == 0

    def test_finds_shortest_distances_through_intermediate_node(self):
        matrix = build_matrix(4, [(0, 1, 1), (1, 2, 2), (0, 2, 4), (2, 3, 1)])

        distance, _ = floyd_warshall(matrix)

        assert distance[0][2] == 3
        assert distance[0][3] == 4

    def test_unreachable_pair_stays_infinite(self):
        matrix = build_matrix(3, [(0, 1, 1)])

        distance, _ = floyd_warshall(matrix)

        assert distance[0][2] == INF
        assert distance[2][0] == INF

    def test_reconstructs_shortest_path(self):
        matrix = build_matrix(4, [(0, 1, 1), (1, 2, 2), (0, 2, 4), (2, 3, 1)])

        _, prev_index = floyd_warshall(matrix)

        assert shortest_path(prev_index, 0, 3) == [0, 1, 2, 3]

    def test_no_path_returns_empty_list(self):
        matrix = build_matrix(3, [(0, 1, 1)])

        _, prev_index = floyd_warshall(matrix)

        assert shortest_path(prev_index, 0, 2) == []

    def test_prefers_direct_edge_over_longer_route(self):
        matrix = build_matrix(3, [(0, 1, 1), (1, 2, 1), (0, 2, 1)])

        distance, _ = floyd_warshall(matrix)

        assert distance[0][2] == 1
