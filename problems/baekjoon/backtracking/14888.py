from sys import stdin

new_input = stdin.readline


def backtracking(arr, op_count_arr, n, op_arr, index, op_count):
    if index == n:
        i = 0
        result = arr[i]
        i += 1

        for op in op_arr:
            if op == 0:
                result += arr[i]
            elif op == 1:
                result -= arr[i]
            elif op == 2:
                result *= arr[i]
            elif op == 3:
                if result < 0:
                    result *= -1
                    result //= arr[i]
                    result *= -1
                else:
                    result //= arr[i]

            i += 1
        return result, result

    min_result = 1_000_000_001
    max_result = -1_000_000_001
    for op in range(4):
        if op_count[op] >= op_count_arr[op]:
            continue

        op_count[op] += 1
        op_arr[index] = op
        candidate_max_result, candidate_min_result = backtracking(arr, op_count_arr, n, op_arr, index + 1, op_count)
        op_count[op] -= 1
        op_arr[index] = -1

        max_result = max(max_result, candidate_max_result)
        min_result = min(min_result, candidate_min_result)

    return max_result, min_result


if __name__ == '__main__':
    n = int(new_input())

    arr = list(map(int, new_input().split(" ")))

    op_count_arr = list(map(int, new_input().split(" ")))

    op_count = [0] * 4

    op_arr = [-1] * (n - 1)

    max_result, min_result = backtracking(arr, op_count_arr, n - 1, op_arr, 0, op_count)
    print(max_result)
    print(min_result)

