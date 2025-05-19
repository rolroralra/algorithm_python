import sys
import heapq


def distance(a: tuple[int, int], b: tuple[int, int]) -> int:
    return (a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1])


if __name__ == '__main__':
    sys.stdin = open('sample_input.txt')
    readline = lambda: sys.stdin.readline().strip()

    N, M = map(int, readline().split())
    arr = []
    for i in range(N):
        x, y = map(int, readline().split())
        arr.append((x, y))

    priority_queue = []
    is_visited = [False] * N
    selected_edge_length = []

    for _ in range(M):
        a, b = map(lambda x: int(x) - 1, readline().split())
        is_visited[a] = True
        is_visited[b] = True

        selected_edge_length.append(distance(arr[a], arr[b]))

        for i in range(N):
            if i == a or i == b or is_visited[i]:
                continue

            heapq.heappush(priority_queue, (distance(arr[i], arr[a]), i, a))
            heapq.heappush(priority_queue, (distance(arr[i], arr[b]), i, b))

    while priority_queue:
        length, curr_index, prev_index = heapq.heappop(priority_queue)

        if is_visited[curr_index]:
            continue

        is_visited[curr_index] = True

        selected_edge_length.append(length)

        if len(selected_edge_length) == N - 1:
            break

        for next_index in range(N):
            if is_visited[next_index]:
                continue

            heapq.heappush(priority_queue, (distance(arr[next_index], arr[curr_index]), next_index, curr_index))

    print(f"{round(sum(map(lambda x: x ** 0.5, selected_edge_length[M:])), 2):.2f}")
