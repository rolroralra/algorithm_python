import sys

class UnionFind:
    def __init__(self, size):
        self.parent = [-1] * size

    def union(self, a, b):
        parent = self.parent
        root_a = self.find(a)
        root_b = self.find(b)

        if root_a == root_b:
            return

        if parent[root_a] > parent[root_b]:
            root_a, root_b = root_b, root_a

        parent[root_a] += parent[root_b]
        parent[root_b] = root_a


    def find(self, a):
        parent = self.parent

        if parent[a] < 0:
            return a

        parent[a] = self.find(parent[a])
        return parent[a]

def kruskal(edge_list: list[tuple[int, int, int]], vertex_count):
    union_find = UnionFind(vertex_count)

    result = 0
    selected_edge_count = 0
    for a, b, length in edge_list:
        root_a = union_find.find(a)
        root_b = union_find.find(b)

        if root_a == root_b:
            continue

        union_find.union(a, b)
        result += length
        selected_edge_count += 1

        if selected_edge_count == vertex_count - 1:
            break

    return result

if __name__ == '__main__':
    sys.stdin = open('sample_input.txt')
    readline = lambda: sys.stdin.readline().strip()

    while True:
        m, n = map(int, readline().split())

        if m == 0 and n == 0:
            break

        edge_list = []
        edge_length_sum = 0
        for _ in range(n):
            a, b, length = map(int, readline().split())

            edge_list.append((a, b, length))
            edge_length_sum += length

        edge_list.sort(key=lambda edge: edge[2])

        print(edge_length_sum - kruskal(edge_list, m))
