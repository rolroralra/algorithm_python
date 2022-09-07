from sys import stdin
import bisect

new_input = stdin.readline

if __name__ == '__main__':
    n = int(new_input())
    arr = list(map(int, new_input().rstrip("\n").split(" ")))

    clone_arr = list(set(arr))

    clone_arr.sort()

    for v in [bisect.bisect_left(clone_arr, v) for v in arr]:
        print(v, end=" ")
