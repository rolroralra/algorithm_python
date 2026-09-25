def scc_by_tarjan(adj_list: list[list[int]]) -> list[list[int]]:
    """
    Strongly Connected Components by Tarjan's Algorithm (single DFS pass, low-link based)

    Args:
        adj_list: directed graph adjacency list

    Returns: list of strongly connected components (each component is a list of vertex indices)
    """
    vertex_count = len(adj_list)
    visit = [0] * vertex_count
    low_link = [0] * vertex_count       # minimum visit sequence reachable from the current node (including itself)
    on_stack = [False] * vertex_count   # whether the current node is in the stack or not
    stack = []
    visit_sequence = 1
    scc_list = []

    def dfs(curr_index: int) -> None:
        nonlocal visit_sequence

        visit[curr_index] = low_link[curr_index] = visit_sequence
        visit_sequence += 1
        stack.append(curr_index)
        on_stack[curr_index] = True

        for next_index in adj_list[curr_index]:
            if visit[next_index] == 0:
                dfs(next_index)

                # Update the low-link value of the current node based on the low-link value of the next node
                low_link[curr_index] = min(low_link[curr_index], low_link[next_index])
            elif on_stack[next_index]:
                # Update the low-link value of the current node based on the visit value of the next node
                low_link[curr_index] = min(low_link[curr_index], visit[next_index])

        if low_link[curr_index] == visit[curr_index]:
            scc = []
            while True:
                node = stack.pop()
                on_stack[node] = False
                scc.append(node)
                if node == curr_index:
                    break
            scc_list.append(scc)

    for i in range(vertex_count):
        if visit[i] == 0:
            dfs(i)

    return scc_list


def scc_by_kosaraju(adj_list: list[list[int]]) -> list[list[int]]:
    """
    Strongly Connected Components by Kosaraju's Algorithm (two-pass DFS over the graph and its reverse)

    Args:
        adj_list: directed graph adjacency list

    Returns: list of strongly connected components (each component is a list of vertex indices)
    """
    vertex_count = len(adj_list)

    is_visited = [False] * vertex_count
    finish_order = []

    def dfs_finish_order(curr_index: int) -> None:
        is_visited[curr_index] = True

        for next_index in adj_list[curr_index]:
            if not is_visited[next_index]:
                dfs_finish_order(next_index)

        # After visiting all reachable nodes from curr_index, add it to the finish order
        finish_order.append(curr_index)

    # First pass: DFS to determine the finish order of nodes
    for i in range(vertex_count):
        if not is_visited[i]:
            dfs_finish_order(i)

    # Create the reversed graph
    reversed_adj_list = [[] for _ in range(vertex_count)]
    for curr_index in range(vertex_count):
        for next_index in adj_list[curr_index]:
            reversed_adj_list[next_index].append(curr_index)

    is_visited = [False] * vertex_count
    scc_list = []

    def dfs_collect(curr_index: int, scc: list[int]) -> None:
        # Add the current node to the current strongly connected component
        is_visited[curr_index] = True
        scc.append(curr_index)

        for next_index in reversed_adj_list[curr_index]:
            if not is_visited[next_index]:
                dfs_collect(next_index, scc)

    # Second pass: DFS on the reversed graph in the order of decreasing finish times
    for curr_index in reversed(finish_order):
        if not is_visited[curr_index]:
            scc = []
            dfs_collect(curr_index, scc)
            scc_list.append(scc)

    return scc_list
