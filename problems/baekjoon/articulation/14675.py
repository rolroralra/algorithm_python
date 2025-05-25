import sys

# sys.setrecursionlimit(10**5)


def articulation_points(adj_list: list[list[int]]) -> list[bool]:
    V = len(adj_list)
    visit = [0] * V
    visit_seq = 1
    is_articulation_point = [False] * V

    def dfs(curr_index: int, prev_index: int = -1) -> int:
        nonlocal adj_list
        nonlocal visit
        nonlocal visit_seq
        nonlocal is_articulation_point

        if visit[curr_index] > 0:
            return visit[curr_index]

        is_root = prev_index == -1
        visit[curr_index] = visit_seq
        visit_seq += 1

        min_visit_seq = visit[curr_index]
        child_count = 0

        for next_index in adj_list[curr_index]:
            if next_index == prev_index:
                continue

            if visit[next_index] == 0:
                child_count += 1
                min_visit_seq_from_child = dfs(next_index, curr_index)

                if not is_root and min_visit_seq_from_child >= visit[curr_index]:
                    is_articulation_point[curr_index] = True
            else:
                min_visit_seq_from_child = visit[next_index]

            min_visit_seq = min(min_visit_seq, min_visit_seq_from_child)

        if is_root and child_count >= 2:
            is_articulation_point[curr_index] = True

        return min_visit_seq

    for i in range(V):
        if visit[i] == 0:
            dfs(i)

    return is_articulation_point


def articulation_edges(adj_list: list[list[int]]) -> list[tuple[int, int]]:
    V = len(adj_list)
    visit = [0] * V
    visit_seq = 1
    articulation_edge_list = []

    def dfs(curr_index: int, prev_index: int = -1) -> int:
        nonlocal adj_list
        nonlocal visit
        nonlocal visit_seq
        nonlocal articulation_edge_list

        if visit[curr_index] > 0:
            return visit[curr_index]

        visit[curr_index] = visit_seq
        visit_seq += 1

        min_visit_seq = visit[curr_index]
        child_count = 0

        for next_index in adj_list[curr_index]:
            if next_index == prev_index:
                continue

            if visit[next_index] == 0:
                min_visit_seq_from_child = dfs(next_index, curr_index)

                if min_visit_seq_from_child > visit[curr_index]:
                    articulation_edge = (curr_index, next_index) if curr_index < next_index else (next_index, curr_index)
                    articulation_edge_list.append(articulation_edge)
            else:
                min_visit_seq_from_child = visit[next_index]

            min_visit_seq = min(min_visit_seq, min_visit_seq_from_child)

        return min_visit_seq

    for i in range(V):
        if visit[i] == 0:
            dfs(i)

    return articulation_edge_list


if __name__ == '__main__':
    sys.stdin = open('sample_input.txt')
    readline = lambda: sys.stdin.readline().strip()

    n = int(readline())

    adj_list = [[] for _ in range(n)]
    edge_list = []
    for _ in range(1, n):
        a, b = map(lambda x: int(x) - 1, readline().split())
        if a > b:
            a, b = b, a

        edge_list.append((a, b))
        adj_list[a].append(b)
        adj_list[b].append(a)

    is_articulation_point = articulation_points(adj_list)
    articulation_edges = set(articulation_edges(adj_list))

    q = int(readline())

    for _ in range(q):
        t, k = map(int, readline().split())

        k -= 1

        if t == 1:
            print("yes" if is_articulation_point[k] else "no")
        elif t == 2:
            print("yes" if edge_list[k] in articulation_edges else "no")
