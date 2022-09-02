from sys import stdin

new_input = stdin.readline

if __name__ == '__main__':
    n = int(new_input())
    arr = list(map(int, new_input().split()))
    x = int(new_input())

    arr.sort()

    answer = 0
    p1 = 0
    p2 = n - 1
    while p1 < p2:
        candidate = arr[p1] + arr[p2]

        if candidate == x:
            answer += 1

        if candidate <= x:
            p1 += 1
        else:
            p2 -= 1

    print(answer)
