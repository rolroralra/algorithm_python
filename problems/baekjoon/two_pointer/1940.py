import sys

if __name__ == '__main__':
    getInput = sys.stdin.readline

    N = int(getInput())
    M = int(getInput())

    arr = list(map(int, getInput().split()))

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

