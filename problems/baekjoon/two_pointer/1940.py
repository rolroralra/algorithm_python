import sys

if __name__ == '__main__':
    readline = sys.stdin.readline

    N = int(readline())
    M = int(readline())

    arr = list(map(int, readline().split()))

    arr.sort()

    startIndex = 0
    endIndex = N - 1
    result = 0
    while startIndex < endIndex:
        value = arr[startIndex] + arr[endIndex]

        if value == M:
            result += 1
            startIndex += 1
            endIndex -= 1
        elif value < M:
            startIndex += 1
        else:
            endIndex -= 1

    print(result)

