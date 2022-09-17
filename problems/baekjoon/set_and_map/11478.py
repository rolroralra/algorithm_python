from sys import stdin
new_input = stdin.readline

if __name__ == '__main__':
    word = new_input().rstrip("\n")
    result = set()
    result.add(word)

    for length in range(1, len(word)):
        for start in range(len(word) - length + 1):
            result.add(word[start:start+length])

    print(len(result))
