import random

import pytest

from algorithm.union_find.union_find import UnionFind


@pytest.mark.unit
class TestUnionFindInstanceApi:
    def test_each_element_starts_as_its_own_root(self):
        uf = UnionFind(5)
        for i in range(5):
            assert uf.find(i) == i

    def test_union_merges_two_sets(self):
        uf = UnionFind(5)
        uf.union(0, 1)

        assert uf.find(0) == uf.find(1)

    def test_unrelated_elements_stay_in_different_sets(self):
        uf = UnionFind(5)
        uf.union(0, 1)

        assert uf.find(0) != uf.find(2)

    def test_union_is_transitive(self):
        uf = UnionFind(5)
        uf.union(0, 1)
        uf.union(1, 2)

        assert uf.find(0) == uf.find(1) == uf.find(2)

    def test_union_of_already_connected_elements_is_noop(self):
        uf = UnionFind(3)
        uf.union(0, 1)
        root_before = uf.find(0)

        uf.union(0, 1)

        assert uf.find(0) == root_before


@pytest.mark.unit
class TestUnionFindInstanceExtras:
    def test_new_element_is_its_own_root(self):
        uf = UnionFind(3)
        assert uf.is_root(0)

    def test_is_root_only_true_for_the_root(self):
        uf = UnionFind(3)
        uf.union(0, 1)
        root = uf.find(0)
        member = 1 if root == 0 else 0

        assert uf.is_root(root)
        assert not uf.is_root(member)

    def test_rank_reflects_set_size_after_unions(self):
        uf = UnionFind(4)
        uf.union(0, 1)
        uf.union(1, 2)

        assert uf.rank(uf.find(0)) == 3

    def test_rank_of_untouched_element_is_one(self):
        uf = UnionFind(3)
        assert uf.rank(0) == 1


@pytest.mark.unit
class TestUnionFindInstanceRandomized:
    @pytest.mark.parametrize("seed", range(10))
    def test_matches_reference_partition(self, seed):
        random.seed(seed)
        size = 30
        uf = UnionFind(size)
        reference = [{i} for i in range(size)]

        def reference_find(i):
            for group in reference:
                if i in group:
                    return group

        for _ in range(100):
            a, b = random.randint(0, size - 1), random.randint(0, size - 1)
            uf.union(a, b)

            group_a = reference_find(a)
            group_b = reference_find(b)
            if group_a is not group_b:
                group_a |= group_b
                reference.remove(group_b)

        for i in range(size):
            for j in range(size):
                same_in_uf = uf.find(i) == uf.find(j)
                same_in_reference = j in reference_find(i)
                assert same_in_uf == same_in_reference


# UnionFind also exposes the same algorithm as classmethods that operate
# directly on a plain `parent` list, without needing an instance.
@pytest.mark.unit
class TestUnionFindStaticApi:
    def test_each_element_starts_as_its_own_root(self):
        parent = [-1] * 5
        for i in range(5):
            assert UnionFind.find_static(parent, i) == i

    def test_union_merges_two_sets(self):
        parent = [-1] * 5
        UnionFind.union_static(parent, 0, 1)

        assert UnionFind.find_static(parent, 0) == UnionFind.find_static(parent, 1)

    def test_unrelated_elements_stay_in_different_sets(self):
        parent = [-1] * 5
        UnionFind.union_static(parent, 0, 1)

        assert UnionFind.find_static(parent, 0) != UnionFind.find_static(parent, 2)

    def test_union_is_transitive(self):
        parent = [-1] * 5
        UnionFind.union_static(parent, 0, 1)
        UnionFind.union_static(parent, 1, 2)

        assert UnionFind.find_static(parent, 0) == UnionFind.find_static(parent, 1) == UnionFind.find_static(parent, 2)

    def test_union_of_already_connected_elements_is_noop(self):
        parent = [-1] * 3
        UnionFind.union_static(parent, 0, 1)
        root_before = UnionFind.find_static(parent, 0)

        UnionFind.union_static(parent, 0, 1)

        assert UnionFind.find_static(parent, 0) == root_before


@pytest.mark.unit
class TestUnionFindStaticRandomized:
    @pytest.mark.parametrize("seed", range(10))
    def test_matches_reference_partition(self, seed):
        random.seed(seed)
        size = 30
        parent = [-1] * size
        reference = [{i} for i in range(size)]

        def reference_find(i):
            for group in reference:
                if i in group:
                    return group

        for _ in range(100):
            a, b = random.randint(0, size - 1), random.randint(0, size - 1)
            UnionFind.union_static(parent, a, b)

            group_a = reference_find(a)
            group_b = reference_find(b)
            if group_a is not group_b:
                group_a |= group_b
                reference.remove(group_b)

        for i in range(size):
            for j in range(size):
                same_in_uf = UnionFind.find_static(parent, i) == UnionFind.find_static(parent, j)
                same_in_reference = j in reference_find(i)
                assert same_in_uf == same_in_reference


@pytest.mark.unit
class TestStaticFindImplementations:
    @pytest.mark.parametrize("find_fn", [UnionFind.find_by_recursive, UnionFind.find_by_loop])
    def test_recursive_and_loop_find_agree(self, find_fn):
        parent = [-1] * 5
        UnionFind.union_static(parent, 0, 1)
        UnionFind.union_static(parent, 1, 2)

        assert find_fn(parent, 0) == find_fn(parent, 2)

    def test_find_static_uses_recursive_implementation_below_threshold(self):
        parent = [-1] * 3
        UnionFind.union_static(parent, 0, 1)

        assert UnionFind.find_static(parent, 0) == UnionFind.find_static(parent, 1)


# Both the instance API (find/union) and the static API (find_static/union_static)
# switch from a recursive to a loop-based find once the structure holds more
# than 1000 elements (sys.getrecursionlimit() is 1000 by default), so the
# dispatch threshold itself needs direct coverage on both APIs.
@pytest.mark.unit
class TestUnionFindInstanceDispatchThreshold:
    def spy_on(self, monkeypatch, name):
        calls = []
        original = getattr(UnionFind, name)

        def spy(self, *args, **kwargs):
            calls.append(args)
            return original(self, *args, **kwargs)

        monkeypatch.setattr(UnionFind, name, spy)
        return calls

    def test_size_at_threshold_uses_recursive_find(self, monkeypatch):
        recursive_calls = self.spy_on(monkeypatch, "_find_by_recursive")
        loop_calls = self.spy_on(monkeypatch, "_find_by_loop")

        uf = UnionFind(1000)
        uf.find(0)

        assert recursive_calls
        assert not loop_calls

    def test_size_above_threshold_uses_loop_find(self, monkeypatch):
        recursive_calls = self.spy_on(monkeypatch, "_find_by_recursive")
        loop_calls = self.spy_on(monkeypatch, "_find_by_loop")

        uf = UnionFind(1001)
        uf.find(0)

        assert loop_calls
        assert not recursive_calls

    def test_correctness_is_preserved_above_the_threshold(self):
        size = 1500
        uf = UnionFind(size)

        for i in range(size - 1):
            uf.union(i, i + 1)

        assert uf.find(0) == uf.find(size - 1)


@pytest.mark.unit
class TestUnionFindStaticDispatchThreshold:
    def spy_on(self, monkeypatch, name):
        calls = []
        original = getattr(UnionFind, name)

        def spy(*args, **kwargs):
            calls.append(args)
            return original(*args, **kwargs)

        monkeypatch.setattr(UnionFind, name, spy)
        return calls

    def test_size_at_threshold_uses_recursive_find(self, monkeypatch):
        recursive_calls = self.spy_on(monkeypatch, "find_by_recursive")
        loop_calls = self.spy_on(monkeypatch, "find_by_loop")

        parent = [-1] * 1000
        UnionFind.find_static(parent, 0)

        assert recursive_calls
        assert not loop_calls

    def test_size_above_threshold_uses_loop_find(self, monkeypatch):
        recursive_calls = self.spy_on(monkeypatch, "find_by_recursive")
        loop_calls = self.spy_on(monkeypatch, "find_by_loop")

        parent = [-1] * 1001
        UnionFind.find_static(parent, 0)

        assert loop_calls
        assert not recursive_calls

    def test_correctness_is_preserved_above_the_threshold(self):
        size = 1500
        parent = [-1] * size

        for i in range(size - 1):
            UnionFind.union_static(parent, i, i + 1)

        assert UnionFind.find_static(parent, 0) == UnionFind.find_static(parent, size - 1)


@pytest.mark.unit
class TestInstanceAndStaticApiAgree:
    def test_same_union_pattern_yields_the_same_partition(self):
        edges = [(i, i + 1) for i in range(0, 20, 2)] + [(i, i + 2) for i in range(0, 20, 4)]

        uf = UnionFind(20)
        parent = [-1] * 20
        for a, b in edges:
            uf.union(a, b)
            UnionFind.union_static(parent, a, b)

        for i in range(20):
            for j in range(20):
                assert (uf.find(i) == uf.find(j)) == (UnionFind.find_static(parent, i) == UnionFind.find_static(parent, j))

    def test_static_api_does_not_mutate_instance_state(self):
        uf = UnionFind(5)
        uf.union(0, 1)

        parent = [-1] * 5
        UnionFind.union_static(parent, 2, 3)

        assert uf.find(0) == uf.find(1)
        assert uf.find(2) != uf.find(3)
