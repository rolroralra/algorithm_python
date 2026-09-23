import sys

import pytest

from algorithm.dijkstra.dijkstra import dijkstra_by_heapq, dijkstra_by_priority_queue, shortest_path

IMPLEMENTATIONS = {
    "priority_queue": dijkstra_by_priority_queue,
    "heapq": dijkstra_by_heapq,
}


def sample_graph() -> list[list[tuple]]:
    # 0 --1--> 1 --2--> 2
    #  \--4--> 2
    #          2 --1--> 3
    return [
        [(1, 1), (2, 4)],
        [(2, 2)],
        [(3, 1)],
        [],
    ]


@pytest.mark.unit
class TestDijkstra:
    @pytest.mark.parametrize("dijkstra", IMPLEMENTATIONS.values(), ids=IMPLEMENTATIONS.keys())
    def test_start_node_distance_is_zero(self, dijkstra):
        distance, _ = dijkstra(sample_graph(), 0)
        assert distance[0] == 0

    @pytest.mark.parametrize("dijkstra", IMPLEMENTATIONS.values(), ids=IMPLEMENTATIONS.keys())
    def test_finds_shortest_distances(self, dijkstra):
        distance, _ = dijkstra(sample_graph(), 0)
        assert distance == [0, 1, 3, 4]

    @pytest.mark.parametrize("dijkstra", IMPLEMENTATIONS.values(), ids=IMPLEMENTATIONS.keys())
    def test_unreachable_node_keeps_infinite_distance(self, dijkstra):
        graph = [[(1, 1)], [], []]

        distance, _ = dijkstra(graph, 0)

        assert distance[2] == sys.maxsize

    @pytest.mark.parametrize("dijkstra", IMPLEMENTATIONS.values(), ids=IMPLEMENTATIONS.keys())
    def test_reconstructs_shortest_path(self, dijkstra):
        _, prev_index = dijkstra(sample_graph(), 0)

        assert shortest_path(prev_index, 3) == [0, 1, 2, 3]

    @pytest.mark.parametrize("dijkstra", IMPLEMENTATIONS.values(), ids=IMPLEMENTATIONS.keys())
    def test_path_to_start_node_is_itself(self, dijkstra):
        _, prev_index = dijkstra(sample_graph(), 0)

        assert shortest_path(prev_index, 0) == [0]

    def test_both_implementations_agree_on_distances(self):
        graph = sample_graph()
        distance_pq, _ = dijkstra_by_priority_queue(graph, 0)
        distance_heap, _ = dijkstra_by_heapq(graph, 0)

        assert distance_pq == distance_heap
