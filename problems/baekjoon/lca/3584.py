import sys

if __name__ == '__main__':
    sys.stdin = open('sample_input.txt')
    readline = lambda: sys.stdin.readline().strip()

    T = int(readline())
    for _ in range(T):
        N = int(readline())

        adj_list = [[] for _ in range(N)]
        LOGN = (N - 1).bit_length()
        parent = [[-1] * (LOGN + 1) for _ in range(N)]
        depth = [-1] * N
        for _ in range(1, N):
            a, b = map(lambda x: int(x) - 1, readline().split())
            adj_list[a].append(b)
            parent[b][0] = a

        for i in range(N):
            if parent[i][0] == -1:
                root_index = i

        stack = []
        depth[root_index] = 0
        stack.append(root_index)

        while stack:
            curr_index = stack.pop()

            for next_index in adj_list[curr_index]:
                if depth[next_index] != -1:
                    continue

                depth[next_index] = depth[curr_index] + 1
                parent[next_index][0] = curr_index
                for depth_level in range(1, LOGN + 1):
                    if parent[next_index][depth_level - 1] != -1:
                        parent[next_index][depth_level] = parent[parent[next_index][depth_level - 1]][depth_level - 1]

                stack.append(next_index)

        def lca(a, b):
            if depth[a] < depth[b]:
                a, b = b, a

            for depth_level in range(LOGN, -1, -1):
                if depth[a] - depth[b] >= (1 << depth_level):
                    a = parent[a][depth_level]

                if depth[a] == depth[b]:
                    break

            if a == b:
                return a

            for depth_level in range(LOGN, -1, -1):
                if parent[a][depth_level] != -1 and parent[a][depth_level] != parent[b][depth_level]:
                    a = parent[a][depth_level]
                    b = parent[b][depth_level]

            return parent[a][0]

        a, b = map(lambda x: int(x) - 1, readline().split())

        print(lca(a, b) + 1)
