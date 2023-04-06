import itertools
import sys

if __name__ == '__main__':
    getInput = sys.stdin.readline

    N, M = map(int, getInput().split())
    arr = []

    for row in range(0, N):
        arr.append(list(map(int, getInput().split())))

    sumArr = [[0] * N for _ in range(N)]

    for couple in itertools.product(range(N), range(N)):
        row, col = couple

        upSum = sumArr[row - 1][col] if row > 0 else 0
        leftSum = sumArr[row][col - 1] if col > 0 else 0
        upLeftSum = sumArr[row - 1][col - 1] if row > 0 and col > 0 else 0

        sumArr[row][col] = upSum + leftSum - upLeftSum + arr[row][col]

    for qIndex in range(M):
        x1, y1, x2, y2 = map(lambda x: int(x) - 1, getInput().split())

        maxX = max(x1, x2)
        maxY = max(y1, y2)
        minX = min(x1, x2)
        minY = min(y1, y2)

        partSums = [
            -sumArr[maxX][minY - 1] if minY > 0 else 0,
            -sumArr[minX - 1][maxY] if minX > 0 else 0,
            sumArr[minX - 1][minY - 1] if minX > 0 and minY > 0 else 0
        ]

        result = sumArr[maxX][maxY] + sum(partSums)

        print(result)
