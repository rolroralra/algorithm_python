if __name__ == '__main__':
    cache = {}

    answer = 1
    i = 1
    cache[1] = 1
    while True:
        answer += (i - 1) * 6
        cache[i] = answer
        i += 1

        if answer > 1000_000_000:
            break

    n = int(input())
    answer = 1

    for key, value in cache.items():
        if n <= value:
            answer = key
            break

    print(answer)

