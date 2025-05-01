import sys
import collections

if __name__ == '__main__':
  readline = sys.stdin.readline

  N, M = map(int, readline().split(maxsplit=2)[:2])

  arr = list(map(int, readline().split(maxsplit=N)[:N]))

  arr[0] %= M
  for i in range(1, N):
    arr[i] = (arr[i] + arr[i - 1]) % M

  count_map = collections.Counter(arr)

  result = count_map[0] + sum([count * (count - 1) // 2 for key, count in count_map.items() if count > 1])

  print(result)

