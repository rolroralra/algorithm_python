import math
from sys import stdin

new_input = stdin.readline


if __name__ == '__main__':
    m = int(new_input())
    n = int(new_input())

    size = n + 1
    is_prime = [True] * size
    is_prime[0] = False
    is_prime[1] = False
    for i in range(2, int(math.sqrt(n)) + 1):
        if not is_prime[i]:
            continue

        for j in range(i * i, size, i):
            is_prime[j] = False

    answer = [0, 0]
    for i in range(m, size):
        if is_prime[i]:
            answer[0] += i
            answer[1] = i if answer[1] == 0 else answer[1]

    if answer[0] == 0:
        print(-1)
    else:
        print(answer[0])
        print(answer[1])
