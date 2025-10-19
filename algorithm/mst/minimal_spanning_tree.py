from enum import Enum
from algorithm.union_find.union_find import UnionFind
from queue import PriorityQueue

class MinimalSpanningTreeAlgorithm(Enum):
    KRUSKAL_ALGORITHM = 1
    PRIM_ALGORITHM = 2

def minimal_spanning_tree(graph, algorithm: MinimalSpanningTreeAlgorithm):
    if algorithm == MinimalSpanningTreeAlgorithm.KRUSKAL_ALGORITHM:
        return mst_kruskal_algorithm(graph)
    elif algorithm == MinimalSpanningTreeAlgorithm.PRIM_ALGORITHM:
        return mst_prim_algorithm(graph)

    raise NotImplementedError("Invalid Algorithm")


def mst_kruskal_algorithm(edge_list: list[tuple[int, int, int]], vertex_size: int = None) -> tuple[int, list[tuple[int, int, int]]]:
    """
    Minimal Spanning Tree by Kruskal Algorithm

    Args:
        edge_list: edge list, while edge consists of (a, b, length)
        vertex_size: vertex size

    Returns: minimal spanning tree length, selected edge list
    """
    edge_list.sort(key=lambda edge: edge[2])

    if vertex_size is None:
        vertex_set = set()
        for a, b, length in edge_list:
            vertex_set.add(a)
            vertex_set.add(b)
        vertex_size = len(vertex_set)

    union_find = UnionFind(vertex_size)

    edge_selected_count = 0
    selected_edge_list = []
    mst_length = 0

    for a, b, length in edge_list:
        if union_find.find(a) != union_find.find(b):
            union_find.union(a, b)
            selected_edge_list.append((a, b, length))
            edge_selected_count += 1
            mst_length += length

        if edge_selected_count == vertex_size - 1:
            break

    return mst_length, selected_edge_list


def mst_prim_algorithm(adj_list: list[list[tuple[int, int]]]) -> tuple[int, list[tuple[int, int, int]]]:
    """
    Minimal Spanning Tree by Prim Algorithm

    Args:
        adj_list: adjacent list, while adjacent list consists of (next_index, length)

    Returns: minimal spanning tree length, selected edge list
    """
    vertex_count = len(adj_list)
    is_visited = [False] * vertex_count
    priority_queue = PriorityQueue()

    mst_length = 0
    selected_edge_list = []

    priority_queue.put((0, 0, -1))
    while not priority_queue.empty():
        curr_edge_length, curr_index, prev_index = priority_queue.get()

        if is_visited[curr_index]:
            continue

        is_visited[curr_index] = True
        if prev_index != -1:
            mst_length += curr_edge_length
            selected_edge_list.append((prev_index, curr_index, curr_edge_length))

        if len(selected_edge_list) == vertex_count - 1:
            break

        for next_index, next_edge_length in adj_list[curr_index]:
            if is_visited[next_index]:
                continue

            priority_queue.put((next_edge_length, next_index, curr_index))

    return mst_length, selected_edge_list
