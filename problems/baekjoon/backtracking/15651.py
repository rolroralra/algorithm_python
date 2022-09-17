from sys import stdin
new_input = stdin.readline


def print_permutation(n, m):
    trace = [0] * m

    __print_permutation(n, m, trace, 0)


def __print_permutation(n, m, trace, count):
    if count == m:
        print(" ".join([str(num) for num in trace]))
        return

    for i in range(n):
        trace[count] = i + 1
        __print_permutation(n, m, trace, count + 1)


# 중복순열 n^m
if __name__ == '__main__':
    n, m = map(int, new_input().split(" "))
    print_permutation(n, m)
