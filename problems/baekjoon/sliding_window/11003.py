import sys
from collections import deque
from collections import namedtuple

Number = namedtuple('Number', ['index', 'value'])

def add_new_number(queue: deque, number: tuple, size: int):
    index, value = number

    while queue and queue[-1][1] > value:
        queue.pop()

    queue.append(number)

    while queue and queue[0][0] <= index - size:
        queue.popleft()

if __name__ == '__main__':
    sys.stdin = open('sample_input.txt')
    readline = sys.stdin.readline

    N, L = map(int, readline().split())

    queue = deque()
    for index, value in enumerate(map(int, readline().split())):
        add_new_number(queue, (index, value), L)
        print(queue[0][1], end=' ')

    arr = list()
