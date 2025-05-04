import sys
import heapq


if __name__ == '__main__':
    readline = sys.stdin.readline

    n = int(readline())

    heap = []
    for _ in range(n):
        for v in list(map(int, readline().split())):
            heapq.heappush(heap, v)

            if len(heap) > n:
                heapq.heappop(heap)

    print(heap[0])
