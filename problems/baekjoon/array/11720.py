import sys

if __name__ == '__main__':
    input = sys.stdin.readline

    N = int(input())

    inputString = input().strip()
    result = 0
    for c in inputString:
        result += int(c)

    print(result)

