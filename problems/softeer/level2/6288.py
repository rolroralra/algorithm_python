import sys

if __name__ == '__main__':
    sys.stdin = open('sample_input.txt', 'r')
    readline = sys.stdin.readline

    W, N = map(int, readline().strip().split())

    arr = []
    for i in range(N):
        weight, price_per_weight = map(int, readline().strip().split())
        arr.append((weight, price_per_weight))

    arr.sort(key=lambda x: x[1], reverse=True)

    result = 0
    for weight, price_per_weight in arr:
        if W <= 0:
            break

        applied_weight = weight if W >= weight else W
        W -= applied_weight

        result += applied_weight * price_per_weight

    print(result)
