def recursive(n: int):
    if n == 3:
        return ["***", "* *", "***"]

    prev_n = n // 3

    prev = recursive(prev_n)

    upper = list(zip(prev, prev, prev))
    middle = list(zip(prev, [" " * prev_n] * prev_n, prev))

    for i in range(len(upper)):
        upper[i] = "".join(upper[i])
        middle[i] = "".join(middle[i])

    lower = upper

    return upper + middle + lower


if __name__ == '__main__':
    n = int(input())

    print('\n'.join(recursive(n)))
