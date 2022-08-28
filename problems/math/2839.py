from sys import stdin
# stdin = open("../../sample_input.txt")
new_input = stdin.readline


def get_count(n):
    for a in range(n // 5, -1, -1):
        remain = n - a * 5
        if remain % 3 == 0:
            return a + remain // 3

    return -1


if __name__ == '__main__':
    n = int(new_input())
    print(get_count(n))
