import sys

def binarysearch(arr, target):
    start_index = 0
    end_index = len(arr) - 1

    while start_index <= end_index:
        mid_index = (start_index + end_index) // 2

        if arr[mid_index] == target:
            return mid_index
        elif arr[mid_index] < target:
            start_index = mid_index + 1
        else:
            end_index = mid_index - 1

    return -(start_index + 1)


if __name__ == '__main__':
    sys.stdin = open('sample_input.txt', 'r')
    readline = sys.stdin.readline

    N = int(readline().strip())
    arr = list(map(int, readline().strip().split()))

    arr.sort()

    M = int(readline().strip())
    for target in map(int, readline().strip().split()):
        print(1 if binarysearch(arr, target) >= 0 else 0)
