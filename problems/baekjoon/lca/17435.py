import sys

if __name__ == '__main__':
    sys.stdin = open('sample_input.txt')
    readline = lambda: sys.stdin.readline().strip()

    m = int(readline())

    original_func = {i + 1: v for i, v in enumerate(map(int, readline().split()))}

    MAX_N = 500_000
    LOGN = (MAX_N - 1).bit_length()
    cache = [[None] * (LOGN + 1) for _ in range(m + 1)]

    def nested_func(input:int, n: int) -> int:
        if cache[input][n] is not None:
            return cache[input][n]

        if n == 0:
            cache[input][n] = original_func[input]
            return cache[input][n]

        prev_result = nested_func(input, n - 1)
        cache[input][n] = nested_func(prev_result, n - 1)
        return cache[input][n]

    Q = int(readline())

    for _ in range(Q):
        n, x = map(int, readline().split())
        remain_n = n
        result = x
        for i in range(LOGN, -1, -1):
            if (1 << i) <= remain_n:
                result = nested_func(result, i)
                remain_n -= (1 << i)

        print(result)
