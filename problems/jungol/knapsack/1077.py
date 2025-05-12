import sys


def knapsack(weights, values, max_weight):
    assert len(weights) == len(values)
    assert max_weight >= 0

    # dp[w] : max values containing w weights
    dp = [0] * (max_weight + 1)

    for weight, value in zip(weights, values):
        for w in range(0, max_weight + 1):
            if w >= weight:
                dp[w] = max(dp[w], dp[w - weight] + value)

    return dp[max_weight]


if __name__ == '__main__':
    readline = sys.stdin.readline
    N, W = map(int, readline().strip().split())

    weights = []
    values = []
    for _ in range(N):
        weight, value = map(int, readline().strip().split())
        weights.append(weight)
        values.append(value)

    print(knapsack(weights, values, W))
