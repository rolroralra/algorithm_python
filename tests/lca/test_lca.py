import pytest

from algorithm.lca.lca import LCA


def build_sample_tree() -> LCA:
    # tree:            0
    #                 / \
    #                1   2
    #               / \   \
    #              3   4   5
    adj = [[1, 2], [0, 3, 4], [0, 5], [1], [1], [2]]
    lca = LCA(6)
    lca.build(adj, root_index=0)
    return lca


@pytest.mark.unit
class TestLcaDepth:
    def test_root_depth_is_zero(self):
        assert build_sample_tree().get_depth(0) == 0

    def test_children_depth_is_one(self):
        lca = build_sample_tree()
        assert lca.get_depth(1) == 1
        assert lca.get_depth(2) == 1

    def test_grandchildren_depth_is_two(self):
        lca = build_sample_tree()
        assert lca.get_depth(3) == 2
        assert lca.get_depth(4) == 2
        assert lca.get_depth(5) == 2


@pytest.mark.unit
class TestLcaQuery:
    def test_siblings_share_parent_as_lca(self):
        lca = build_sample_tree()
        assert lca.lca(3, 4) == 1

    def test_cousins_share_root_as_lca(self):
        lca = build_sample_tree()
        assert lca.lca(3, 5) == 0

    def test_node_and_its_parent(self):
        lca = build_sample_tree()
        assert lca.lca(3, 1) == 1

    def test_node_and_its_ancestor(self):
        lca = build_sample_tree()
        assert lca.lca(3, 0) == 0

    def test_node_with_itself(self):
        lca = build_sample_tree()
        assert lca.lca(4, 4) == 4

    def test_order_of_arguments_does_not_matter(self):
        lca = build_sample_tree()
        assert lca.lca(3, 5) == lca.lca(5, 3)


@pytest.mark.unit
class TestLcaDeeperTree:
    def test_long_chain(self):
        # 0 - 1 - 2 - 3 - 4 (a straight line)
        adj = [[1], [0, 2], [1, 3], [2, 4], [3]]
        lca = LCA(5)
        lca.build(adj, root_index=0)

        assert lca.lca(4, 0) == 0
        assert lca.lca(3, 4) == 3
        assert [lca.get_depth(i) for i in range(5)] == [0, 1, 2, 3, 4]
