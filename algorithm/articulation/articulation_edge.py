def articulation_edges(adj_list: list[list[int]]) -> list[tuple[int, int]]:
    V = len(adj_list)

    articulation_edge_list = []
    visit = [0] * V
    visit_seq = 1

    def dfs(curr_index: int, prev_index: int = -1) -> int:
        nonlocal adj_list
        nonlocal visit
        nonlocal visit_seq

        if visit[curr_index] > 0:
            return visit[curr_index]

        visit[curr_index] = visit_seq
        visit_seq += 1
        min_visit_seq = visit[curr_index]

        for next_index in adj_list[curr_index]:
            if next_index == prev_index:
                continue

            if visit[next_index] == 0:
                min_visit_seq_from_child = dfs(next_index, curr_index)

                if min_visit_seq_from_child > visit[curr_index]:
                    articulation_edge = (curr_index, next_index) if curr_index <= next_index else (next_index, curr_index)
                    articulation_edge_list.append(articulation_edge)
            else:
                min_visit_seq_from_child = visit[next_index]

            min_visit_seq = min(min_visit_seq, min_visit_seq_from_child)

        return min_visit_seq

    for i in range(V):
        if visit[i] == 0:
            dfs(i)

    return articulation_edge_list
