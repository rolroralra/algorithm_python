from sys import stdin
new_input = stdin.readline


def print_permutation(n, m):
    is_visited = [False] * n

    __print_permutation(n, m, is_visited, 0, 0)


def __print_permutation(n, m, is_visited, start_index, count):
    if count == m:
        for i in range(n):
            if is_visited[i]:
                print(i + 1, end=" ")

        print()
        return

    for i in range(start_index, n):
        if is_visited[i]:
            continue

        is_visited[i] = True
        __print_permutation(n, m, is_visited, i + 1, count + 1)
        is_visited[i] = False


if __name__ == '__main__':
    n, m = map(int, new_input().split(" "))
    print_permutation(n, m)
