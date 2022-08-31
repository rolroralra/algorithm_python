from sys import stdin

new_input = stdin.readline


def check_generator(n, candidate):
    result = candidate

    while candidate > 0:
        result += candidate % 10
        candidate //= 10

    return n == result


if __name__ == '__main__':
    n_str = new_input()
    n = int(n_str)

    answer = 0
    for candidate in range(n - 9 * len(n_str), n + 1):
        if check_generator(n, candidate):
            answer = candidate
            break

    print(answer)
