from collections import deque

def topological_sort_by_dfs_recursive(adj_list: list[list[int]]):
    stack = list()
    is_visited = [False] * len(adj_list)
    is_finished = [False] * len(adj_list)
    has_cycle = False

    def dfs(adj_list: list[list[int]], curr_index:int, is_visited: list[bool], is_finished: list[bool], result: list[int]):
        nonlocal has_cycle
        is_visited[curr_index] = True

        for next_index in adj_list[curr_index]:
            # If the next node has not been visited, perform DFS on it
            if not is_visited[next_index]:
                dfs(adj_list, next_index, is_visited, is_finished, result)
            # If the next node has been visited but not finished, a cycle is detected
            elif not is_finished[next_index]:
                has_cycle = True
                return

        # Mark the current node as finished and add it to the result stack
        is_finished[curr_index] = True
        result.append(curr_index)

    for index in range(len(adj_list)):
        if not is_visited[index]:
            dfs(adj_list, index, is_visited, is_finished, stack)

    # Reverse the stack to get the topological order
    sorted_result = []
    while stack:
        sorted_result.append(stack.pop())

    return sorted_result, has_cycle


def topological_sort_by_indegree(adj_list: list[list[int]]):
    in_degree = [0] * len(adj_list)

    # Initialize in-degree for each vertex
    for indices in adj_list:
        for index in indices:
            in_degree[index] += 1

    queue = deque()
    for index in range(len(in_degree)):
        # Add vertices with in-degree of 0 to the queue
        if in_degree[index] == 0:
            queue.append(index)

    sorted_result = []
    while queue:
        # Process the vertex with in-degree of 0
        curr_index = queue.popleft()
        sorted_result.append(curr_index)

        for next_index in adj_list[curr_index]:
            # Decrease the in-degree of the adjacent vertices
            in_degree[next_index] -= 1

            # If the in-degree becomes 0, add it to the queue
            if in_degree[next_index] == 0:
                queue.append(next_index)

    has_cycle = len(sorted_result) < len(adj_list)

    return sorted_result, has_cycle
