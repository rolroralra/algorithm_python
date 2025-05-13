import sys

if __name__ == '__main__':
    readline = lambda: sys.stdin.readline().strip()

    N = int(readline())

    unit_size = (2 ** N) + 1

    print(unit_size ** 2)
