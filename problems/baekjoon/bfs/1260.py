import sys
import collections

def dfs(graph, start_index):
    is_visited = [False] * len(graph)
    stack = [start_index]

    while stack:
        curr_index = stack.pop()

        if is_visited[curr_index]:
            continue

        is_visited[curr_index] = True

        print(curr_index, end=' ')

        for next_index in graph[curr_index]:
            if is_visited[next_index]:
                continue

            stack.append(next_index)

    print()


def bfs(graph, start_index):
    is_visited = [False] * len(graph)
    is_visited[start_index] = True
    queue = collections.deque([start_index])

    while queue:
        curr_index = queue.popleft()
        print(curr_index, end=' ')

        for next_index in graph[curr_index]:
            if is_visited[next_index]:
                continue

            queue.append(next_index)
            is_visited[next_index] = True

    print()


if __name__ == '__main__':
    sys.stdin = open('sample_input.txt', 'r')
    readline = sys.stdin.readline

    N, M, V = map(int, readline().strip().split())

    graph = [[] for _ in range(N + 1)]

    for _ in range(M):
        a, b = map(int, readline().strip().split())

        graph[a].append(b)
        graph[b].append(a)

    for i in range(N + 1):
        graph[i].sort(reverse=True)

    dfs(graph, V)

    for i in range(N + 1):
        graph[i].sort()

    bfs(graph, V)
