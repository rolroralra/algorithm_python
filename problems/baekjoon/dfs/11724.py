import sys


def dfs(graph, is_visited, start_index):
    stack = [start_index]
    is_visited[start_index] = True

    while stack:
        curr_index = stack.pop()

        for next_index in graph[curr_index]:
            if is_visited[next_index]:
                continue

            stack.append(next_index)
            is_visited[next_index] = True


if __name__ == '__main__':
    sys.stdin = open('sample_input.txt', 'r')
    readline = sys.stdin.readline

    N, M = map(int, readline().strip().split())

    graph = [[] for _ in range(N)]

    for _ in range(M):
        u, v = map(lambda x: int(x) - 1, readline().strip().split())

        graph[u].append(v)
        graph[v].append(u)

    result = 0
    is_visited = [False] * N

    for start_index in range(N):
        if is_visited[start_index]:
            continue

        dfs(graph, is_visited, start_index)
        result += 1

    print(result)
