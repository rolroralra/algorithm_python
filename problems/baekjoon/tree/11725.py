import sys

sys.setrecursionlimit(10**6)
if __name__ == '__main__':
    sys.stdin = open('sample_input.txt')
    readline = lambda: sys.stdin.readline().strip()

    N = int(readline())

    adj_list = [[] for _ in range(N)]
    for _ in range(1, N):
        a, b = map(lambda x: int(x) - 1, readline().split())
        adj_list[a].append(b)
        adj_list[b].append(a)


    is_visited = [False] * N
    parent = [-1] * N

    def dfs(curr_index, prev_index=-1):
        is_visited[curr_index] = True

        for next_index in adj_list[curr_index]:
            if is_visited[next_index]:
                continue

            dfs(next_index, curr_index)

        parent[curr_index] = prev_index

    dfs(0)

    for i in range(1, N):
        print(parent[i] + 1)
