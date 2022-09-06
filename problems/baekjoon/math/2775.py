from sys import stdin
stdin = open("../../../sample_input.txt")
new_input = stdin.readline

if __name__ == '__main__':
    t = int(new_input())
    for test_case in range(t):
        k = int(new_input())
        n = int(new_input())

        dp = [0] * n

        for i in range(n):
            dp[i] = i + 1

        for i in range(k):
            for j in range(1, n):
                dp[j] += dp[j - 1]

        print(dp[n - 1])
