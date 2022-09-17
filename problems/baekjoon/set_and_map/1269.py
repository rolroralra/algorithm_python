from sys import stdin
new_input = stdin.readline

if __name__ == '__main__':
    n, m = map(int, new_input().split(" "))
    set_a = set(map(int, new_input().split(" ")))
    set_b = set(map(int, new_input().split(" ")))

    print(len(set_a.symmetric_difference(set_b)))
    # print(len(set_a ^ set_b))
