import sys

def floyd_warshall(adj_matrix: list[list[int]]):
    vertex_count = len(adj_matrix)
    INF = sys.maxsize

    distance = [[INF] * vertex_count for _ in range(vertex_count)]
    prev_index = [[-1] * vertex_count for _ in range(vertex_count)]

    for i in range(vertex_count):
        distance[i][i] = 0

        for j in range(vertex_count):
            if adj_matrix[i][j] < INF:
                distance[i][j] = adj_matrix[i][j]
                prev_index[i][j] = i

    for k in range(vertex_count):
        for i in range(vertex_count):
            if distance[i][k] == INF:
                continue

            for j in range(vertex_count):
                if distance[k][j] == INF:
                    continue

                new_distance = distance[i][k] + distance[k][j]
                if new_distance < distance[i][j]:
                    distance[i][j] = new_distance
                    prev_index[i][j] = prev_index[k][j]

    return distance, prev_index


def shortest_path(prev_index: list[list[int]], start_index, target_index):
    if prev_index[start_index][target_index] == -1:
        return []

    stack = []
    index = target_index

    while index != -1:
        stack.append(index)
        index = prev_index[start_index][index]

    stack.reverse()

    return stack
