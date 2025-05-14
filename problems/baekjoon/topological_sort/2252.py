import sys
from collections import deque

if __name__ == '__main__':
    sys.stdin = open('sample_input.txt', 'r')
    readline = lambda: sys.stdin.readline().strip()

    N, M = map(int, readline().split())

    adj_list = [[] for _ in range(N + 1)]
    in_degree = [0] * (N + 1)

    for _ in range(M):
        a, b = map(int, readline().split())
        adj_list[a].append(b)
        in_degree[b] += 1

    queue = deque([i for i in range(1, N + 1) if in_degree[i] == 0])
    sorted_result = []
    while queue:
        curr_index = queue.popleft()
        sorted_result.append(curr_index)

        for next_index in adj_list[curr_index]:
            in_degree[next_index] -= 1

            if in_degree[next_index] == 0:
                queue.append(next_index)

    has_cycle = len(sorted_result) != len(adj_list)

    print(" ".join(map(str, sorted_result)))
