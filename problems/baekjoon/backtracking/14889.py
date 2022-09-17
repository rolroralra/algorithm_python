from sys import stdin

new_input = stdin.readline


def backtracking(arr, index, a_team, b_team, team_size, total_member_count):
    if index == total_member_count:
        return abs(calculateTeamScore(a_team, arr) - calculateTeamScore(b_team, arr))

    result = 100 * 20 * 20
    if len(a_team) < team_size:
        a_team.append(index)
        result = min(result, backtracking(arr, index + 1, a_team, b_team, team_size, total_member_count))
        a_team.pop()

    if len(b_team) < team_size:
        b_team.append(index)
        result = min(result, backtracking(arr, index + 1, a_team, b_team, team_size, total_member_count))
        b_team.pop()

    return result


def calculateTeamScore(team, arr):
    result = 0
    for i in range(0, len(team) - 1):
        for j in range(i + 1, len(team)):
            m1 = team[i]
            m2 = team[j]
            result += arr[m1][m2] + arr[m2][m1]

    return result


if __name__ == '__main__':
    n = int(new_input())

    arr = [list(map(int, new_input().split(" "))) for i in range(n)]

    print(backtracking(arr, 0, [], [], n // 2, n))
