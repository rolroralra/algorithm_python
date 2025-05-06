import sys


def check_relationship(graph, max_depth=4):
    return any(__check_relationship(graph, [False] * len(graph), start_index, 0, max_depth)
               for start_index in range(len(graph)))


def __check_relationship(graph, is_visited, curr_index, curr_depth, max_depth):
    if curr_depth >= max_depth:
        return True

    is_visited[curr_index] = True
    next_depth = curr_depth + 1

    for next_index in graph[curr_index]:
        if is_visited[next_index]:
            continue

        if __check_relationship(graph, is_visited, next_index, next_depth, max_depth):
            return True

    is_visited[curr_index] = False

    return False


if __name__ == '__main__':
    sys.stdin = open('sample_input.txt', 'r')
    readline = sys.stdin.readline

    N, M = map(int, readline().strip().split())

    graph = [[] for _ in range(N)]

    for _ in range(M):
        a, b = map(int, readline().strip().split())
        graph[a].append(b)
        graph[b].append(a)

    print(1 if check_relationship(graph, 4) else 0)
