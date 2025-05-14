import sys

def union(parent, a, b):
    root_a = find(parent, a)
    root_b = find(parent, b)

    if root_a == root_b:
        return

    if parent[root_a] > parent[root_b]:
        root_a, root_b = root_b, root_a

    parent[root_a] += parent[root_b]
    parent[root_b] = root_a


def find(parent, a):
    if parent[a] < 0:
        return a

    parent[a] = find(parent, parent[a])
    return parent[a]

if __name__ == '__main__':
    sys.stdin = open('sample_input.txt', 'r')
    readline = lambda: sys.stdin.readline().strip()

    N = int(readline())
    M = int(readline())

    graph = [list(map(int, readline().split())) for _ in range(N)]

    parent = [-1] * N

    for i in range(N):
        for j in range(N):
            if graph[i][j] == 1:
                union(parent, i, j)

    print("YES" if len({find(parent, city) for city in map(lambda x: int(x) - 1, readline().split())}) == 1 else "NO")
