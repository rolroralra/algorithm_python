from sys import stdin
new_input = stdin.readline

if __name__ == '__main__':
    n = int(new_input())
    card_set = set(map(int, new_input().split(" ")))

    m = int(new_input())
    print(" ".join("1" if v in card_set else "0" for v in list(map(int, new_input().split(" ")))))
