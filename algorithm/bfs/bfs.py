from collections import deque

def bfs(graph, start_index):
    is_visited = [False] * len(graph)

    queue = deque([start_index])
    is_visited[start_index] = True

    while queue:
        curr_index = queue.popleft()

        # visit process

        for next_index in graph[curr_index]:
            if is_visited[next_index]:
                continue

            queue.append(next_index)
            is_visited[next_index] = True
