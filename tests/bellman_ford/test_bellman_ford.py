import sys

import pytest

from algorithm.bellman_ford.bellman_ford import bellman_ford, shortest_path


@pytest.mark.unit
class TestBellmanFord:
    def test_start_node_distance_is_zero(self):
        distance, _, _ = bellman_ford([(0, 1, 1), (1, 2, 2)], 0)
        assert distance[0] == 0

    def test_finds_shortest_distances(self):
        edges = [(0, 1, 1), (1, 2, 2), (0, 2, 4), (2, 3, 1)]

        distance, _, has_negative_cycle = bellman_ford(edges, 0)

        assert distance == [0, 1, 3, 4]
        assert has_negative_cycle is False

    def test_reconstructs_shortest_path(self):
        edges = [(0, 1, 1), (1, 2, 2), (0, 2, 4), (2, 3, 1)]

        _, prev_index, _ = bellman_ford(edges, 0)

        assert shortest_path(prev_index, 3) == [0, 1, 2, 3]

    def test_handles_negative_edge_weights(self):
        edges = [(0, 1, 4), (0, 2, 5), (1, 2, -3)]

        distance, _, has_negative_cycle = bellman_ford(edges, 0)

        assert distance == [0, 4, 1]
        assert has_negative_cycle is False

    def test_detects_negative_cycle(self):
        edges = [(0, 1, 1), (1, 2, -3), (2, 0, 1)]

        _, _, has_negative_cycle = bellman_ford(edges, 0)

        assert has_negative_cycle is True

    def test_unreachable_node_keeps_infinite_distance(self):
        edges = [(0, 1, 1), (2, 3, 1)]

        distance, _, _ = bellman_ford(edges, 0)

        assert distance[2] == sys.maxsize
        assert distance[3] == sys.maxsize
