import sys
import heapq
from collections import deque

dx = [1, -1, 0, 0]
dy = [0, 0, 1, -1]

def bfs(graph, start_row, start_col):
    queue = deque()
    queue.append((start_row, start_col))
    graph[start_row][start_col] = 0
    total_visit_count = 1

    while queue:
        curr_row, curr_col = queue.popleft()

        for ddx, ddy in zip(dx, dy):
            next_row = curr_row + ddx
            next_col = curr_col + ddy

            if next_row < 0 or next_row >= len(graph) or next_col < 0 or next_col >= len(graph[0]):
                continue

            if graph[next_row][next_col] == 1:
                queue.append((next_row, next_col))
                graph[next_row][next_col] = 0
                total_visit_count += 1

    return total_visit_count


if __name__ == '__main__':
    readline = lambda: sys.stdin.readline().strip()

    N = int(readline())

    arr = []

    for _ in range(N):
        arr.append([int(c) for c in readline()])

    group_count = 0
    group_size_list = []
    for row in range(N):
        for col in range(N):
            if arr[row][col] == 1:
                group_count += 1
                heapq.heappush(group_size_list, bfs(arr, row, col))

    print(group_count)
    while group_size_list:
        print(heapq.heappop(group_size_list))
