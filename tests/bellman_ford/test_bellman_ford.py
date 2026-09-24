import sys

import pytest

from algorithm.bellman_ford import bellman_ford as bellman_ford_module
from algorithm.bellman_ford.bellman_ford import bellman_ford, shortest_path


def chain_prev_index(size: int) -> list[int]:
    """prev_index for a straight chain 0 -> 1 -> 2 -> ... -> size - 1."""
    return [-1] + list(range(size - 1))


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


# `shortest_path` switches from a recursive to a loop-based path reconstruction once
# `prev_index` holds 500 or more elements (`len(prev_index) < 500` in
# bellman_ford.py:33). The threshold sits well below sys.getrecursionlimit() (1000 by
# default) because a worst-case, path-shaped graph recurses as deep as the path is
# long, and the caller's own call stack (e.g. pytest's) already consumes part of that
# budget -- see test_recursive_implementation_handles_worst_case_chain_at_threshold
# below for the regression coverage that would have caught this when the threshold
# used to be 1000.
@pytest.mark.unit
class TestShortestPathDispatchThreshold:
    def spy_on(self, monkeypatch, name):
        calls = []
        original = getattr(bellman_ford_module, name)

        def spy(*args, **kwargs):
            calls.append(args)
            return original(*args, **kwargs)

        monkeypatch.setattr(bellman_ford_module, name, spy)
        return calls

    def test_size_below_threshold_uses_recursive_implementation(self, monkeypatch):
        recursive_calls = self.spy_on(monkeypatch, "_shorted_path_by_recursive")
        loop_calls = self.spy_on(monkeypatch, "_shortest_path_by_loop")

        prev_index = [-1] * 499
        shortest_path(prev_index, 0)

        assert recursive_calls
        assert not loop_calls

    def test_size_at_threshold_uses_loop_implementation(self, monkeypatch):
        recursive_calls = self.spy_on(monkeypatch, "_shorted_path_by_recursive")
        loop_calls = self.spy_on(monkeypatch, "_shortest_path_by_loop")

        prev_index = [-1] * 500
        shortest_path(prev_index, 0)

        assert loop_calls
        assert not recursive_calls

    def test_size_above_threshold_uses_loop_implementation(self, monkeypatch):
        recursive_calls = self.spy_on(monkeypatch, "_shorted_path_by_recursive")
        loop_calls = self.spy_on(monkeypatch, "_shortest_path_by_loop")

        prev_index = [-1] * 501
        shortest_path(prev_index, 0)

        assert loop_calls
        assert not recursive_calls

    def test_recursive_implementation_reconstructs_short_chain(self):
        size = 400
        prev_index = chain_prev_index(size)

        assert shortest_path(prev_index, size - 1) == list(range(size))

    def test_loop_implementation_reconstructs_long_chain_without_recursion_limit(self):
        # A chain far longer than sys.getrecursionlimit() would overflow the recursive
        # implementation; the loop-based one must handle it without issue.
        size = 5000
        prev_index = chain_prev_index(size)

        assert shortest_path(prev_index, size - 1) == list(range(size))

    def test_recursive_implementation_handles_worst_case_chain_at_threshold(self):
        # Regression coverage for the recursion-depth bug this threshold fixes: a
        # worst-case (path-shaped) graph whose chain length sits right at the
        # recursive/loop boundary must NOT raise RecursionError, even under a test
        # runner's own call stack overhead.
        size = 499
        prev_index = chain_prev_index(size)

        assert shortest_path(prev_index, size - 1) == list(range(size))
