import sys

def articulation_points(adj_list: list[list[int]], root_index: int = 0) -> list[int]:
    vertex_count = len(adj_list)
    is_articulation_point = [False] * vertex_count
    visit = [0] * vertex_count
    visit_seq = 1

    def dfs(curr_index: int, is_root: bool=False) -> int:
        nonlocal is_articulation_point
        nonlocal adj_list
        nonlocal visit
        nonlocal visit_seq

        if visit[curr_index] > 0:
            return visit[curr_index]

        visit[curr_index] = visit_seq
        visit_seq += 1

        min_visit_seq_arround = visit[curr_index]
        dfs_spanning_tree_child_count = 0

        for next_index in adj_list[curr_index]:
            if visit[next_index] == 0:
                dfs_spanning_tree_child_count += 1
                min_visit_seq_from_child = dfs(next_index)

                if not is_root and min_visit_seq_from_child >= visit[curr_index]:
                    is_articulation_point[curr_index] = True
            else:
                min_visit_seq_from_child = visit[next_index]

            min_visit_seq_arround = min(min_visit_seq_arround, min_visit_seq_from_child)

        if is_root:
            is_articulation_point[curr_index] = (dfs_spanning_tree_child_count >= 2)

        return min_visit_seq_arround

    for i in range(vertex_count):
        if visit[i] == 0:
            dfs(i, True)

    return [i for i, is_articulation in enumerate(is_articulation_point) if is_articulation]


if __name__ == '__main__':
    sys.stdin = open('sample_input.txt')
    readline = lambda: sys.stdin.readline().strip()

    V, E = map(int, readline().split())

    adj_list = [[] for _ in range(V)]
    for _ in range(E):
        a, b = map(lambda x: int(x) - 1, readline().split())

        adj_list[a].append(b)
        adj_list[b].append(a)

    result = [i for i, v in articulation_points(adj_list) if v]

    print(len(result))
    print(" ".join(str(i + 1) for i in result))
