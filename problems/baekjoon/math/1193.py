import sys

input = sys.stdin.readline

if __name__ == '__main__':
    x = int(input())

    sum = 0
    n = 1
    while x > sum:
        sum += n
        n += 1

    b = sum - x + 1
    a = n - b

    if n % 2 == 0:
        a, b = b, a

    print(f'{a}/{b}')