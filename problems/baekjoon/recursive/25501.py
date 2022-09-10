from sys import stdin

new_input = stdin.readline


def is_palindrome(input_string: str, left=0, right=None):
    if right is None:
        right = len(input_string) - 1

    if left >= right:
        return 1, 1
    elif input_string[left] != input_string[right]:
        return 0, 1
    else:
        result, count = is_palindrome(input_string, left + 1, right - 1)
        return result, count + 1


if __name__ == '__main__':
    t = int(new_input())
    for i in range(t):
        result, count = is_palindrome(new_input().rstrip("\n"))
        print(result, count)
