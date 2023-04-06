import sys

if __name__ == '__main__':
    getInput = sys.stdin.readline

    N, M = map(int, getInput().split(" ", 2))
    arr = list(map(int, getInput().split(" ", N)))
    "".ljust()

    sumArr = []

    currentSum = 0
    for n in arr:
        currentSum += n
        sumArr.append(currentSum)

    for i in range(0, M):
        start, end = map(lambda x: int(x) - 1, getInput().split(" ", 2))
        print(sumArr[end] - (sumArr[start - 1] if start > 0 else 0))
