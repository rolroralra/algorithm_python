def hanoi(n:int, start, mid, end, buffer: list):
    if n == 1:
        buffer.append(f"{start} {end}")
        return 1

    answer = 0
    answer += hanoi(n - 1, start, end, mid, buffer)
    answer += 1

    buffer.append(f"{start} {end}")

    answer += hanoi(n - 1, mid, start, end, buffer)

    return answer


if __name__ == '__main__':
    n = int(input())

    buffer = []
    print(hanoi(n, 1, 2, 3, buffer))
    print("\n".join(buffer))

