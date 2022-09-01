from sys import stdin

new_input = stdin.readline


if __name__ == '__main__':
    n = int(new_input())

    count_arr = [0] * 10_001

    for i in range(n):
        count_arr[int(new_input())] += 1

    count = 0
    for i in range(1, 10_000_001):
        if count >= n:
            break

        if count_arr[i] == 0:
            continue

        for j in range(count_arr[i]):
            print(i)
            count += 1
