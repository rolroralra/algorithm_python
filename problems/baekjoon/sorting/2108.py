from sys import stdin

new_input = stdin.readline


if __name__ == '__main__':
    n = int(new_input())

    arr = [0] * n
    count_map = dict()
    max_count = 0
    max_frequent_value_arr = []
    for i in range(n):
        value = int(new_input())
        arr[i] = value
        count_map.setdefault(value, 0)
        count_map[value] += 1

        if max_count == count_map[value]:
            max_frequent_value_arr.append(value)
        elif max_count < count_map[value]:
            max_count = count_map[value]
            max_frequent_value_arr.clear()
            max_frequent_value_arr.append(value)

    max_frequent_value_arr.sort()
    arr.sort()

    print(round(sum(arr) / n))
    print(arr[n // 2])
    print(max_frequent_value_arr[1] if len(max_frequent_value_arr) >= 2 else max_frequent_value_arr[0])
    print(arr[-1] - arr[0])



