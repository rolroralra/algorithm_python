from sys import stdin

new_input = stdin.readline


if __name__ == '__main__':
    n, k = map(int, new_input().split())
    arr = list(map(int, new_input().split()))

    arr.sort(reverse=True)

    print(arr[k - 1])
