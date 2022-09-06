from sys import stdin

new_input = stdin.readline

if __name__ == '__main__':
    n = int(new_input())

    arr = [list(map(int, new_input().rstrip("\n").split(" "))) for i in range(n)]

    arr = list(map(lambda l: (l[0], l[1]), arr))
    arr.sort()
    for x, y in arr:
        print(x, y)



