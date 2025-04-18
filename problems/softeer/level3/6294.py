import sys

#5 3
#10 50 20 70 100
#1 3
#3 4
#1 5

sys.stdin = open('sample_input.txt')
input = sys.stdin.readline


def read_line(sep=" "):
    return list(map(int, input().split(sep)))

N, K = read_line()

arr = read_line()

for i in range(K):
    a, b = list(map(lambda x: x - 1, read_line()))
    sum_result = sum([arr[j] for j in range(a, b + 1)])
    mean_result = sum_result / (b + 1 - a)
    result = round(mean_result, 2)
    print(f"{result:.2f}")

#26.67
#45.00
#50.00
