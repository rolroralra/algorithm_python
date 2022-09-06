from sys import stdin

new_input = stdin.readline


def process(arr, i, j, first, candidate):
    check_word = [first, "W" if first == "B" else "B"]

    pivot_index = 0

    result = 0
    for row in range(i, i + 8):
        for col in range(j, j + 8):
            if arr[row][col] != check_word[pivot_index]:
                result += 1

            if result >= candidate:
                return candidate

            pivot_index = 1 - pivot_index
        pivot_index = 1 - pivot_index

    return result


if __name__ == '__main__':
    n, m = map(int, new_input().split())

    arr = [[c for c in new_input().rstrip("\n")] for i in range(n)]

    answer = m * n
    for i in range(0, n - 7):
        for j in range(0, m - 7):
            answer = min(answer, process(arr, i, j, "W", answer))
            answer = min(answer, process(arr, i, j, "B", answer))

    print(answer)

    enumerate(new_input().rstrip())


# import sys
# from itertools import accumulate as acc
# input = sys.stdin.readline
# n, m = map(int, input().split())
# y = [[0]*(m+1)]
# for i in range(n):
#     ac = [0]
#     ac.extend(acc([((s=='W')+i+j) % 2 for j, s in enumerate(input().rstrip())]))
#     y.append([k + j for k, j in zip(ac, y[-1])])
#
# res = 32
# for i in range(n-7):
#     for j in range(m-7):
#         u = y[i+8][j+8]-y[i+8][j]-y[i][j+8]+y[i][j]
#         res = min(res, u, 64-u)
# print(res)