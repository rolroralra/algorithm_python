import sys
import heapq


if __name__ == '__main__':
    sys.stdin = open('sample_input.txt')
    readline = lambda: sys.stdin.readline().strip()

    N = int(readline())
    M = int(readline())

    adj_list = [[] for _ in range(N)]
    for _ in range(M):
        a, b, length = map(int, readline().split())

        adj_list[a - 1].append((b - 1, length))
        adj_list[b - 1].append((a - 1, length))

    is_visited = [False] * N
    queue = []
    heapq.heappush(queue, (0, 0, -1))
    mst_length = 0
    selected_edge_list = []

    while queue:
        length, curr_index, prev_index = heapq.heappop(queue)

        if is_visited[curr_index]:
            continue

        is_visited[curr_index] = True
        if prev_index != -1:
            mst_length += length
            selected_edge_list.append((prev_index, curr_index, length))

        if len(selected_edge_list) == N - 1:
            break

        for next_index, length in adj_list[curr_index]:
            if is_visited[next_index]:
                continue

            heapq.heappush(queue, (length, next_index, curr_index))

    print(mst_length)
