from sys import stdin
from queue import PriorityQueue
import heapq

new_input = stdin.readline

if __name__ == '__main__':
    n = int(new_input())

    heap = []
    for _ in range(n):
        for v in list(map(int, new_input().split())):
            heapq.heappush(heap, v)

            if len(heap) > n:
                heapq.heappop(heap)

    print(heap[0])
