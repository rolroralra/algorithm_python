import sys

input = sys.stdin.readline

if __name__ == '__main__':
    n = int(input())
    checked = dict()

    for i in range(n):
        checked[int(input())] = True

    for v in range(-1_000_000, 1_000_001):
        if v in checked:
            print(v)
