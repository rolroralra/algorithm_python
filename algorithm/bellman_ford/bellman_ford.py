import sys

def bellman_ford(edge_list: list[tuple], start_index: int):
    vertex_set = {}
    for a, b, length in edge_list:
        vertex_set.add(a)
        vertex_set.add(b)

    vertex_count = len(vertex_set)

    INF = sys.maxsize
    distance = [INF] * vertex_count
    prev_index = [-1] * vertex_count
    has_negative_cycle = False

    for loop_index in range(vertex_count):
        for from_index, to_index, length in edge_list:
            if distance[from_index] < INF and distance[from_index] + length < distance[to_index]:
                distance[to_index] = distance[from_index] + length
                prev_index[to_index] = from_index

                if loop_index == vertex_count - 1:
                    has_negative_cycle = True
                    break

    return distance, prev_index, has_negative_cycle


def shortest_path(prev_index: list[int], target_index):
    vertex_count = len(prev_index)
    stack = []

    index = target_index
    while index != -1:
        stack.append(index)
        index = prev_index[index]

    stack.reverse()

    return stack
