from sys import stdin

new_input = stdin.readline


if __name__ == '__main__':
    n = int(new_input())

    count = 0
    answer = 666
    for i in range(666, 1_000_000_000):
        if "666" in str(i):
            count += 1

            if count == n:
                answer = i
                break

    print(answer)
