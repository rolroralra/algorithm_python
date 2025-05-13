import sys

if __name__ == '__main__':
    readline = lambda: sys.stdin.readline().strip()

    n = int(readline())
    arr = list(map(int, readline().split()))

    max_size = max(arr)

    max_r = min(max_size, 100)

    result = 1
    for r in range(2, max_r + 1):
        result = max(result, sum(1 for size in arr if size % r == 0))

        if result == n:
            break

    print(result)
