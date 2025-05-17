import sys
import heapq
from queue import PriorityQueue

if __name__ == '__main__':
    sys.stdin = open('sample_input.txt', 'r')
    readline = lambda: sys.stdin.readline().strip()

    V, E = map(int, readline().split())

    start_index = int(readline()) - 1

    graph = [[] for _ in range(V)]

    for _ in range(E):
        a, b, w = map(int, readline().split())
        graph[a - 1].append((b - 1, w))

    is_visited = [False] * V
    distance = [-1] * V # sys.maxsize
    prev_index = [-1] * V
    distance[start_index] = 0
    queue = []
    heapq.heappush(queue, (0, start_index))

    while queue:
        curr_distance, curr_index = heapq.heappop(queue)

        if is_visited[curr_index]:
            continue

        is_visited[curr_index] = True

        for next_index, edge_length in graph[curr_index]:
            new_distance = distance[curr_index] + edge_length

            if distance[next_index] == -1 or new_distance < distance[next_index]:
                distance[next_index] = new_distance
                prev_index[next_index] = curr_index
                heapq.heappush(queue, (distance[next_index], next_index))

    for index in range(V):
        print(distance[index] if distance[index] != -1 else "INF")
