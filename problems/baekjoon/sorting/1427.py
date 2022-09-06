import functools
from sys import stdin

new_input = stdin.readline

if __name__ == '__main__':
    arr = list(new_input())[0:-1]
    arr.sort(reverse=True)
    print(functools.reduce(lambda x, y: x + y, arr))

