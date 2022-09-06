from sys import stdin

new_input = stdin.readline


def backtracking(card_list, is_visited, curr_count, curr_index, curr_sum, m):
    if curr_count >= 3:
        return curr_sum

    answer = -1

    for next_index in range(curr_index, len(card_list)):
        next_sum = curr_sum + card_list[next_index]

        if is_visited[next_index] or next_sum > m:
            continue

        is_visited[next_index] = True
        answer = max(answer, backtracking(card_list, is_visited, curr_count + 1, next_index + 1, next_sum, m))
        is_visited[next_index] = False

    return answer


if __name__ == '__main__':
    n, m = map(int, new_input().split())

    card_list = list(map(int, new_input().split()))
    is_visited = [False] * len(card_list)
    print(backtracking(card_list, is_visited, 0, 0, 0, m))

