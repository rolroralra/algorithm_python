from sys import stdin
new_input = stdin.readline


def print_permutation(n, m):
    isVisited = [False] * n
    trace = [0] * m

    __print_permutation(n, m, isVisited, trace, 0)


def __print_permutation(n, m, isVisited, trace, count):
    if count == m:
        print(" ".join(map(str, trace)))
        return

    for i in range(n):
        if isVisited[i]:
            continue

        isVisited[i] = True
        trace[count] = i + 1
        __print_permutation(n, m, isVisited, trace, count + 1)
        isVisited[i] = False

# 순열 nPr
if __name__ == '__main__':
    n, m = map(int, new_input().split(" "))
    print_permutation(n, m)
