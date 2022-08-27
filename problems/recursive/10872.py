import sys

# sys.stdin = open('../../sample_input.txt')
input = sys.stdin.readline


def factorial(n=0):
    if n <= 1:
        return 1

    return n * factorial(n - 1)


if __name__ == '__main__':
    n = int(input())
    print(factorial(n))


