import sys
import math


def is_prime(number):
    return all(number % i != 0 for i in range(2, math.isqrt(number) + 1))


def dfs(number, max_depth, result):
    number_str = str(number)
    curr_depth = len(number_str)

    if curr_depth >= max_depth:
        result.append(number)
        return number

    for i in [1, 3, 5, 7, 9]:
        next_number = int(number_str + str(i))

        if is_prime(next_number):
            dfs(next_number, max_depth, result)


if __name__ == '__main__':
    readline = sys.stdin.readline

    N = int(readline().strip())

    result = []
    for i in [2, 3, 5, 7]:
        dfs(i, N, result)


    for prime in result:
        print(prime)
