class UnionFind:
    def __init__(self, size: int):
        assert size > 0
        self.parent = [-1] * size


    def union(self, a: int, b: int):
        union(self.parent, a, b)


    def find(self, a: int):
        return find(self.parent, a)


def union(parent: list[int], a: int, b: int):
    root_a = find(parent, a)
    root_b = find(parent, b)

    if root_a == root_b:
        return

    if parent[root_a] > parent[root_b]:
        root_a, root_b = root_b, root_a

    parent[root_a] += parent[root_b]
    parent[root_b] = root_a


def find(parent: list[int], a: int):
    return find_by_recursive(parent, a)


def find_by_recursive(parent: list[int], a: int):
    if parent[a] < 0:
        return a

    parent[a] = find_by_recursive(parent, parent[a])
    return parent[a]


def find_by_loop(parent: list[int], a: int):
    root = a
    while parent[root] >= 0:
        root = parent[root]

    index = a
    while index != root:
        next_index = parent[index]
        parent[index] = root
        index = next_index

    return root
