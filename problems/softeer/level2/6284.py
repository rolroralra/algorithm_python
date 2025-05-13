import sys

if __name__ == '__main__':
    readline = lambda: sys.stdin.readline().strip()

    K, P, N = map(int, readline().split())

    MOD = 1_000_000_007

    result = K % MOD
    for _ in range(N):
        result = (result * P) % MOD

    print(result)
