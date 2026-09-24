import pytest

from algorithm.strong_connected_components.strongly_connected_components import (
    scc_by_kosaraju,
    scc_by_tarjan,
)

IMPLEMENTATIONS = {
    "tarjan": scc_by_tarjan,
    "kosaraju": scc_by_kosaraju,
}


def as_component_set(scc_list: list[list[int]]) -> set[frozenset[int]]:
    return {frozenset(component) for component in scc_list}


@pytest.mark.unit
class TestStronglyConnectedComponents:
    @pytest.mark.parametrize("scc", IMPLEMENTATIONS.values(), ids=IMPLEMENTATIONS.keys())
    def test_single_vertex_no_edges(self, scc):
        assert as_component_set(scc([[]])) == {frozenset({0})}

    @pytest.mark.parametrize("scc", IMPLEMENTATIONS.values(), ids=IMPLEMENTATIONS.keys())
    def test_two_vertex_cycle_is_one_component(self, scc):
        adj_list = [[1], [0]]

        assert as_component_set(scc(adj_list)) == {frozenset({0, 1})}

    @pytest.mark.parametrize("scc", IMPLEMENTATIONS.values(), ids=IMPLEMENTATIONS.keys())
    def test_acyclic_graph_each_vertex_is_its_own_component(self, scc):
        adj_list = [[1], [2], []]

        assert as_component_set(scc(adj_list)) == {frozenset({0}), frozenset({1}), frozenset({2})}

    @pytest.mark.parametrize("scc", IMPLEMENTATIONS.values(), ids=IMPLEMENTATIONS.keys())
    def test_single_cycle_across_all_vertices(self, scc):
        adj_list = [[1], [2], [3], [0]]

        assert as_component_set(scc(adj_list)) == {frozenset({0, 1, 2, 3})}

    @pytest.mark.parametrize("scc", IMPLEMENTATIONS.values(), ids=IMPLEMENTATIONS.keys())
    def test_two_cycles_connected_by_a_bridge_edge(self, scc):
        # cycle {0,1,2} -> bridge 2->3 -> cycle {3,4,5}
        adj_list = [[1], [2], [0, 3], [4], [5], [3]]

        assert as_component_set(scc(adj_list)) == {
            frozenset({0, 1, 2}),
            frozenset({3, 4, 5}),
        }

    @pytest.mark.parametrize("scc", IMPLEMENTATIONS.values(), ids=IMPLEMENTATIONS.keys())
    def test_self_loop_is_its_own_component(self, scc):
        adj_list = [[0], [0]]

        assert as_component_set(scc(adj_list)) == {frozenset({0}), frozenset({1})}

    @pytest.mark.parametrize("scc", IMPLEMENTATIONS.values(), ids=IMPLEMENTATIONS.keys())
    def test_disconnected_components_evaluated_independently(self, scc):
        adj_list = [[1], [0], [3], [2]]

        assert as_component_set(scc(adj_list)) == {
            frozenset({0, 1}),
            frozenset({2, 3}),
        }

    @pytest.mark.parametrize("scc", IMPLEMENTATIONS.values(), ids=IMPLEMENTATIONS.keys())
    def test_all_vertices_are_covered_exactly_once(self, scc):
        adj_list = [[1], [2], [0, 3], [4], [5, 3], [3]]

        components = scc(adj_list)
        flattened = [vertex for component in components for vertex in component]

        assert sorted(flattened) == list(range(len(adj_list)))
