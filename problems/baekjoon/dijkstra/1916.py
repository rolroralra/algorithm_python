import sys
from queue import PriorityQueue

if __name__ == '__main__':
    sys.stdin = open('sample_input.txt', 'r')
    readline = lambda: sys.stdin.readline().strip()

    N = int(readline())
    M = int(readline())

    adj_list = [[] for _ in range(N)]

    for _ in range(M):
        from_index, to_index, edge_length = map(int, readline().split())
        adj_list[from_index - 1].append((to_index - 1, edge_length))

    start_index, end_index = map(lambda x: int(x) - 1, readline().split())

    distance = [sys.maxsize] * N
    is_visited = [False] * N
    prev_index = [-1] * N

    priority_queue = PriorityQueue()
    distance[start_index] = 0
    priority_queue.put((0, start_index))

    while not priority_queue.empty():
        curr_distance, curr_index = priority_queue.get()

        if is_visited[curr_index]:
            continue

        is_visited[curr_index] = True

        for next_index, edge_length in adj_list[curr_index]:
            new_distance = distance[curr_index] + edge_length

            if new_distance < distance[next_index]:
                distance[next_index] = new_distance
                prev_index[next_index] = curr_index
                priority_queue.put((distance[next_index] , next_index))

    print(distance[end_index])
