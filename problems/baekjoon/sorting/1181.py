from sys import stdin

new_input = stdin.readline

if __name__ == '__main__':
    n = int(new_input())
    arr = [new_input().rstrip("\n") for i in range(n)]

    arr.sort(key=lambda s: (len(s), s))

    word_set = set()
    for word in arr:
        if word not in word_set:
            print(word)
            word_set.add(word)

