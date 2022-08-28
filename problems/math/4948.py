import math
from sys import stdin

new_input = stdin.readline

if __name__ == '__main__':

    max_size = 123_456 * 2
    is_prime = [True] * (max_size + 1)

    is_prime[0] = False
    is_prime[1] = False

    for i in range(2, int(math.sqrt(max_size)) + 1):
        if not is_prime[i]:
            continue

        for j in range(i * i, max_size + 1, i):
            is_prime[j] = False

    while True:
        n = int(new_input())

        if n == 0:
            break

        count = 0
        for i in range(n + 1, 2 * n + 1):
            if is_prime[i]:
                count += 1

        print(count)
