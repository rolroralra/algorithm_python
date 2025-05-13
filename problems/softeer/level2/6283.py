import sys


def order_check(arr):
    if all(arr[i - 1] < arr[i] for i in range(1, len(arr))):
        return "ascending"
    elif all(arr[i - 1] > arr[i] for i in range(1, len(arr))):
        return "descending"
    else:
        return "mixed"


if __name__ == '__main__':
    readline = lambda: sys.stdin.readline().strip()

    arr = list(map(int, readline().split()))

    print(order_check(arr))
