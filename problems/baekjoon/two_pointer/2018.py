import sys

if __name__ == '__main__':
    getInput = sys.stdin.readline

    N = int(getInput())

    startNumber = 1
    endNumber = 1
    sumResult = 1
    result = 0

    while startNumber <= endNumber <= N and startNumber <= N:
        if sumResult == N:
            result += 1
            endNumber += 1
            sumResult += endNumber if endNumber <= N else 0
        elif sumResult < N:
            endNumber += 1
            sumResult += endNumber if endNumber <= N else 0
        else:
            sumResult -= startNumber
            startNumber += 1

    print(result)
