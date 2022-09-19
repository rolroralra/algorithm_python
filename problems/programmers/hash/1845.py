from sys import stdin

new_input = stdin.readline


def solution(nums):
    return min(len(nums) // 2, len(set(nums)))


def solution_1(nums):
    n = len(nums) // 2
    monster_set = set(nums)
    return len(monster_set) if len(monster_set) < n else n


if __name__ == '__main__':
    print(solution([3, 1, 2, 3]))
    print(solution([3, 3, 3, 2, 2, 4]))
    print(solution([3, 3, 3, 2, 2, 2]))
