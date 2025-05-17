import sys

if __name__ == '__main__':
    sys.stdin = open('sample_input.txt', 'r')
    readline = lambda: sys.stdin.readline().strip()

    N, M = map(int, readline().split())

    edge_list = []
    for _ in range(M):
        a, b, length = map(int, readline().split())

        edge_list.append((a - 1, b - 1, length))

    distance = [sys.maxsize] * N
    prev_index = [-1] * N
    has_negative_cycle = False

    distance[0] = 0
    for loop_index in range(N):
        for a, b, length in edge_list:
            if distance[a] < sys.maxsize and distance[a] + length < distance[b]:
                distance[b] = distance[a] + length
                prev_index[b] = a

                if loop_index == N - 1:
                    has_negative_cycle = True
                    break

    if has_negative_cycle:
        print(-1)
    else:
        for target_index in range(1, N):
            print(distance[target_index] if distance[target_index] < sys.maxsize else -1)
