def isProfit(a, b, c, answer):
    return a + (b - c) * answer < 0


def process(a, b, c):
    d = c - b
    if d <= 0:
        return -1

    return int(a / d) + 1


if __name__ == '__main__':
    inputs = [int(input_string) for input_string in input().split(" ")]

    a = inputs[0]
    b = inputs[1]
    c = inputs[2]

    print(process(a, b, c))
