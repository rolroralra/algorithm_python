def knapsack(weights, values, max_weight, one_or_zero=False):
    assert len(weights) == len(values)
    assert max_weight >= 0

    if one_or_zero:
        return knapsackWithOneOrZero(weights, values, max_weight)
    else:
        return knapsackWithSufficientStock(weights, values, max_weight)


def knapsackWithSufficientStock(weights, values, max_weight):
    assert len(weights) == len(values)
    assert max_weight >= 0

    # dp[w] : max values containing w weights
    dp = [0] * (max_weight + 1)

    for weight, value in zip(weights, values):
        for w in range(0, max_weight + 1):
            if w >= weight:
                dp[w] = max(dp[w], dp[w - weight] + value)

    return dp[max_weight]


def knapsackWithOneOrZero(weights, values, max_weight):
    assert len(weights) == len(values)
    assert max_weight >= 0

    before_dp = [0] * (max_weight + 1)
    after_dp = [0] * (max_weight + 1)

    for weight, value in zip(weights, values):
        for w in range(max_weight, -1, -1):
            if w < weight:
                after_dp[w] = before_dp[w]
            else:
                after_dp[w] = max(before_dp[w], before_dp[w - weight] + value)

        before_dp, after_dp = after_dp, before_dp

    return before_dp[max_weight]
