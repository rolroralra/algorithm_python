def check(value):
    isChecked = set()

    prev = ""
    for curr in value:
        if curr != prev:
            if curr in isChecked:
                return False

            isChecked.add(curr)
            prev = curr

    return True


if __name__ == '__main__':
    n = int(input())
    answer = 0
    for _ in range(0, n):
        if check(input()):
            answer += 1

    print(answer)
