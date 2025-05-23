def dfs(adjacent_list, is_visited, start_index=0, recursive=False):
    if recursive:
        print("Calling Recursive DFS")
        __dfs_by_recursive(adjacent_list, is_visited, start_index)
    else:
        print("Calling DFS")
        __dfs_smoothly_by_stack(adjacent_list, is_visited, start_index)


def __dfs_smoothly_by_stack(adjacent_list, is_visited, start_index=0):
    stack = [start_index]
    is_visited[start_index] = True

    while stack:
        curr_index = stack.pop()

        # visit process

        for next_index in adjacent_list[curr_index]:
            if is_visited[next_index]:
                continue

            stack.append(next_index)
            is_visited[next_index] = True


def __dfs_exactly_by_stack(adjacent_list, is_visited, start_index=0):
    stack = [start_index]

    while stack:
        curr_index = stack.pop()

        if is_visited[curr_index]:
            continue

        # visit process
        is_visited[curr_index] = True


        for next_index in adjacent_list[curr_index]:
            if is_visited[next_index]:
                continue

            stack.append(next_index)


def __dfs_by_recursive(adjacent_list, is_visited, curr_index=0):
    is_visited[curr_index] == True

    # visit process

    for next_index in adjacent_list[curr_index]:
        if is_visited[next_index]:
            continue

        __dfs_by_recursive(adjacent_list, is_visited, next_index)


if __name__ == '__main__':
    graph = [[1, 2], [0, 3], [0, 4], [1], [2]]

    is_visited = [False] * len(graph)

    dfs(graph, is_visited, 0, True)

    print(is_visited)
