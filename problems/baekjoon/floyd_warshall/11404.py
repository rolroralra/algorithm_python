import sys


if __name__ == '__main__':
    sys.stdin = open('sample_input.txt', 'r')
    readline = lambda: sys.stdin.readline().strip()

    n = int(readline())
    m = int(readline())
    INF = sys.maxsize
    adj_matrix = [[INF] * n for _ in range(n)]

    for _ in range(m):
        a, b, length = map(int, readline().split())
        adj_matrix[a - 1][b - 1] = min(adj_matrix[a - 1][b - 1], length)

    distance = [[INF] * n for _ in range(n)]
    prev_index = [[-1] * n for _ in range(n)] # prev_index[i][j] = (last - 1)'s index on i to j path

    for i in range(n):
        distance[i][i] = 0

        for j in range(n):
            if adj_matrix[i][j] < INF:
                distance[i][j] = adj_matrix[i][j]
                prev_index[i][j] = i


    for k in range(n):
        for i in range(n):
            if distance[i][k] == INF:
                continue
            for j in range(n):
                if distance[k][j] == INF:
                    continue

                new_distance = distance[i][k] + distance[k][j]

                if new_distance < distance[i][j]:
                    distance[i][j] = new_distance
                    prev_index[i][j] = prev_index[k][j]

    for i in range(n):
        for j in range(n):
            if distance[i][j] == INF:
                print(0, end=' ')
            else:
                print(distance[i][j], end=' ')

        print()
