from sys import stdin

stdin = open('../../sample_input.txt')
input = stdin.readline


def allocate_room(h, w, n):
    if n > h * w:
        return None

    height = (n - 1) % h + 1
    width = (n - 1) // h + 1
    return f"{height}{width:02d}"


if __name__ == '__main__':
    t = int(input())

    for test_case in range(t):
        h, w, n = map(int, input().split(" "))

        print(allocate_room(h, w, n))
