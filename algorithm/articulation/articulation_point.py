def articulation_points(adj_list: list[list[int]]) -> list[int]:
    vertex_count = len(adj_list)
    is_articulation_point = [False] * vertex_count
    visit = [0] * vertex_count
    visit_sequence = 1

    def dfs(curr_index: int, is_root: bool = False) -> int:
        """
        Params:
            curr_index: current node index
            is_root: whethere current node is root or not
        Return:
            if curr_index is not visited, minimum visit sequence of child nodes including current node itself
            else, visit sequence of current node
        """
        nonlocal adj_list
        nonlocal is_articulation_point
        nonlocal visit
        nonlocal visit_sequence

        if visit[curr_index] > 0:
            return visit[curr_index]

        visit[curr_index] = visit_sequence
        visit_sequence += 1

        min_visit_sequence = visit[curr_index]
        child_count = 0

        for next_index in adj_list[curr_index]:
            if visit[next_index] == 0:
                child_count += 1
                min_visit_seq_from_child = dfs(next_index)

                if not is_root and min_visit_seq_from_child >= visit[curr_index]:
                    is_articulation_point[curr_index] = True
            else:
                min_visit_seq_from_child = visit[next_index]

            min_visit_sequence = min(min_visit_sequence, min_visit_seq_from_child)

        if is_root and child_count >= 2:
            is_articulation_point[curr_index] = True

        return min_visit_sequence

    for i in range(vertex_count):
        if visit[i] == 0:
            dfs(i, True)

    return [i for i, is_articulation in enumerate(is_articulation_point) if is_articulation]
