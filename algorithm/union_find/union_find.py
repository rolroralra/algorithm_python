class UnionFind:
    def __init__(self, size: int):
        assert size > 0
        self.parent = [-1] * size

    def union(self, a: int, b: int):
        root_a = self.find(a)
        root_b = self.find(b)

        if root_a == root_b:
            return

        # Union by rank (size)
        if self.rank(root_a) < self.rank(root_b):
            root_a, root_b = root_b, root_a

        self.parent[root_a] += self.parent[root_b]
        self.parent[root_b] = root_a

    def find(self, a: int):
        if len(self.parent) > 1000:
            return self._find_by_loop(a)

        return self._find_by_recursive(a)

    def rank(self, a: int):
        root_a = self.find(a)
        return -self.parent[root_a]

    def is_root(self, a: int):
        return self.parent[a] < 0

    def _find_by_recursive(self, a: int):
        if self.is_root(a):
            return a

        # Path compression
        self.parent[a] = self._find_by_recursive(self.parent[a])
        return self.parent[a]

    def _find_by_loop(self, a: int):
        root = a
        while not self.is_root(root):
            root = self.parent[root]

        # Path compression
        index = a
        while index != root:
            next_index = self.parent[index]
            self.parent[index] = root
            index = next_index

        return root

    @classmethod
    def union_static(cls, parent: list[int], a: int, b: int):
        root_a = cls.find_static(parent, a)
        root_b = cls.find_static(parent, b)

        if root_a == root_b:
            return

        # Union by rank (size)
        if parent[root_a] > parent[root_b]:
            root_a, root_b = root_b, root_a

        parent[root_a] += parent[root_b]
        parent[root_b] = root_a

    @classmethod
    def find_static(cls, parent: list[int], a: int):
        if len(parent) > 1000:
            return cls.find_by_loop(parent, a)

        return cls.find_by_recursive(parent, a)

    @classmethod
    def find_by_recursive(cls, parent: list[int], a: int):
        if parent[a] < 0:
            return a

        # Path compression
        parent[a] = cls.find_by_recursive(parent, parent[a])
        return parent[a]

    @classmethod
    def find_by_loop(cls, parent: list[int], a: int):
        root = a
        while parent[root] >= 0:
            root = parent[root]

        # Path compression
        index = a
        while index != root:
            next_index = parent[index]
            parent[index] = root
            index = next_index

        return root
