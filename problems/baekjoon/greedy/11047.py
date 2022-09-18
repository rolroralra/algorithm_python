from sys import stdin

new_input = stdin.readline

if __name__ == '__main__':
    n, k = map(int, new_input().split(" "))

    arr = [int(new_input()) for i in range(n)]
    arr.reverse()

    result = 0
    for coin in arr:
        if k >= coin:
            result += k // coin
            k %= coin

    print(result)