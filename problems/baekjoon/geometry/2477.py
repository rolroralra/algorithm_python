from sys import stdin

readline = stdin.readline


if __name__ == '__main__':
    k = int(readline())

    arr = [tuple(map(int, readline().split(" ")))[1] for i in range(6)]

    even_max = max(arr[0::2])
    odd_max = max(arr[1::2])

    base_area = even_max * odd_max

    for index in range(0, 6):
        even_index = index if index % 2 == 0 else (index + 1) % 6
        odd_index = index if index % 2 == 1 else (index + 1) % 6

        if arr[even_index] != even_max or arr[odd_index] != odd_max:
            continue

        excluded_index_1 = (index + 3) % 6
        excluded_index_2 = (excluded_index_1 + 1) % 6

        excluded_area = arr[excluded_index_1] * arr[excluded_index_2]
        result = (base_area - excluded_area) * k
        break

    print(result)
