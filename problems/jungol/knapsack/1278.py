import sys

if __name__ == '__main__':
    sys.stdin = open('sample_input.txt', 'r')
    readline = lambda: sys.stdin.readline().strip()

    N, W = map(int, readline().split())

    weights = []
    values = []
    for _ in range(N):
        weight, value = map(int, readline().split())
        weights.append(weight)
        values.append(value)

    # dp[0][w] : max values before taking once
    # dp[1][w] : max values after taking once
    dp = [[0] * (W + 1) for _ in range(2)]

    for weight, value in zip(weights, values):
        for w in range(W, -1, -1):
            if w < weight:
                dp[1][w] = dp[0][w]
            else:
                dp[1][w] = max(dp[0][w], dp[0][w - weight] + value)

        dp[0], dp[1] = dp[1], dp[0]

    print(dp[0][W])
