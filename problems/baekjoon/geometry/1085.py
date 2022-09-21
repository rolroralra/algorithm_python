from sys import stdin

readline = stdin.readline

if __name__ == '__main__':
    x, y, w, h = map(int, readline().split(" "))

    print(min(x, w - x, y, h - y))