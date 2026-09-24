import sys

def bellman_ford(edge_list: list[tuple], start_index: int) -> tuple[list[int], list[int], bool]:
    vertex_set = set()
    for a, b, length in edge_list:
        vertex_set.add(a)
        vertex_set.add(b)

    vertex_count = len(vertex_set)

    INF = sys.maxsize
    distance = [INF] * vertex_count
    distance[start_index] = 0
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

def shortest_path(prev_index: list[int], target_index) -> list[int]:
    # A worst-case (path-shaped) graph recurses as deep as the path is long, so the
    # threshold must stay well below sys.getrecursionlimit() (1000 by default) to leave
    # headroom for the caller's own call stack.
    if len(prev_index) < 500:
        return _shorted_path_by_recursive(prev_index, target_index)

    return _shortest_path_by_loop(prev_index, target_index)

def _shortest_path_by_loop(prev_index: list[int], target_index) -> list[int]:
    stack = []

    index = target_index
    while index != -1:
        stack.append(index)
        index = prev_index[index]

    stack.reverse()

    return stack

def _shorted_path_by_recursive(prev_index: list[int], target_index) -> list[int]:
    if target_index == -1:
        return []

    path = _shorted_path_by_recursive(prev_index, prev_index[target_index])
    path.append(target_index)

    return path

def print_shortest_path(prev_index: list[int], target_index) -> None:
    path = shortest_path(prev_index, target_index)
    print(" -> ".join(str(index) for index in path))
