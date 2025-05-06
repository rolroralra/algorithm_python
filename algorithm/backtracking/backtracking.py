def backtracking(graph, is_visited, curr_index, *args):
    if prunning():
        return

    is_visited[curr_index] = True

    for next_index in graph[curr_index]:
        if is_visited[next_index]:
            continue

        backtracking(graph, is_visited, next_index, *args)

    is_visited[curr_index] = False


def prunning():
    return False
