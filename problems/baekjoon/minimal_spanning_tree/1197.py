import sys

class UnionFind:
    def __init__(self, size: int):
        assert size > 0
        self.parent = [-1] * size


    def union(self, a: int, b: int):
        root_a = self.find(a)
        root_b = self.find(b)

        if root_a == root_b:
            return

        if self.parent[root_a] > self.parent[root_b]:
            root_a, root_b = root_b, root_a

        self.parent[root_a] += self.parent[root_b]
        self.parent[root_b] = root_a


    def find(self, a: int):
        if self.parent[a] < 0:
            return a

        self.parent[a] = self.find(self.parent[a])
        return self.parent[a]


if __name__ == '__main__':
    sys.stdin = open('sample_input.txt')
    readline = lambda: sys.stdin.readline().strip()

    V, E = map(int, readline().split())

    edge_list = []
    for _ in range(E):
        a, b, length = map(int, readline().split())
        edge_list.append(((a - 1), (b - 1), length))

    union_find = UnionFind(V)

    edge_list.sort(key=lambda x: x[2])

    edge_count = 0
    result = 0
    for a, b, length in edge_list:
        if union_find.find(a) == union_find.find(b):
            continue

        union_find.union(a, b)
        result += length
        edge_count += 1

        if edge_count == V - 1:
            break

    print(result)
