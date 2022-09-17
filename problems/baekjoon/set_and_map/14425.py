import functools
from sys import stdin
new_input = stdin.readline

if __name__ == '__main__':
    n, m = map(int, new_input().split(" "))

    word_set = set(new_input().rstrip("\n") for i in range(n))

    input_word_list = list(new_input().rstrip("\n") for i in range(m))

    print(functools.reduce(lambda x, y: x + y, map(lambda x: 1 if x in word_set else 0, input_word_list)))
