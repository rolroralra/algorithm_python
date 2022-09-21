from sys import stdin

readline = stdin.readline

if __name__ == '__main__':

    while True:
        input_list = list(map(int, readline().split(" ")))
        input_list.sort()

        a, b, c = map(lambda x: x, input_list)

        if a == 0 and b == 0 and c == 0:
            break

        print("right" if a ** 2 + b ** 2 == c ** 2 else "wrong")