from sys import stdin

# stdin = open('../../sample_input.txt')
input = stdin.readline

if __name__ == '__main__':
    a, b, v = map(int, input().split(" "))

    print(a, b, v)