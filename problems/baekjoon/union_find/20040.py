import sys

class UnionFind:
    def __init__(self, size):
        self.parent = [-1] * size

    def union(self, a, b):
        parent = self.parent

        root_a = self.find(a)
        root_b = self.find(b)

        if root_a == root_b:
            return False

        if parent[root_a] > parent[root_b]:
            root_a, root_b = root_b, root_a

        parent[root_a] += parent[root_b]
        parent[root_b] = root_a

        return True


    def find(self, a):
        parent = self.parent

        if parent[a] < 0:
            return a

        parent[a] = self.find(parent[a])
        return parent[a]


if __name__ == '__main__':
    sys.stdin = open('sample_input.txt')
    readline = lambda: sys.stdin.readline().strip()

    n, m = map(int, readline().split())

    union_find = UnionFind(n)

    result = 0
    for i in range(1, m + 1):
        a, b = map(int, readline().split())

        if not union_find.union(a, b):
            result = i
            break

    print(result)
