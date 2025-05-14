import sys
from collections import deque


def topological_sort(adj_list):
    in_degree = [0] * len(adj_list)

    for child_indices in adj_list:
        for child_index in child_indices:
            in_degree[child_index] += 1

    sorted_result = []

    queue = deque([index for index in range(len(adj_list)) if in_degree[index] == 0])

    while queue:
        curr_index = queue.popleft()
        sorted_result.append(curr_index)

        for next_index in adj_list[curr_index]:
            in_degree[next_index] -= 1

            if in_degree[next_index] == 0:
                queue.append(next_index)

    return sorted_result, len(sorted_result) < len(adj_list)


if __name__ == '__main__':
    sys.stdin = open('sample_input.txt', 'r')
    readline = lambda: sys.stdin.readline().strip()

    N = int(readline())
    adj_list = [[] for _ in range(N)]
    times = [0] * N

    for index in range(N):
        inputs = readline().split()

        times[index] = int(inputs[0])

        for from_index in map(lambda x: int(x) - 1, inputs[1:-1]):
            adj_list[from_index].append(index)

    in_degree = [0] * len(adj_list)

    for child_indices in adj_list:
        for child_index in child_indices:
            in_degree[child_index] += 1

    sorted_result = []
    spend_times = times.copy()
    queue = deque([index for index in range(len(adj_list)) if in_degree[index] == 0])

    while queue:
        curr_index = queue.popleft()
        sorted_result.append(curr_index)

        for next_index in adj_list[curr_index]:
            in_degree[next_index] -= 1

            spend_times[next_index] = max(spend_times[next_index], spend_times[curr_index] + times[next_index])
            if in_degree[next_index] == 0:
                queue.append(next_index)

    for spend_time in spend_times:
        print(spend_time)
