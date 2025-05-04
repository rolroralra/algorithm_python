import sys

def is_good_number(index, nums):
  target = nums[index]
  start_index = 0
  end_index = len(nums) - 1

  while start_index < end_index:
    if start_index == index:
      start_index += 1
      continue

    if end_index == index:
      end_index -= 1
      continue

    sum_result = nums[start_index] + nums[end_index]

    if sum_result == target:
      return True
    elif sum_result > target:
      end_index -= 1
    else:
      start_index += 1

  return False


if __name__ == '__main__':
  sys.stdin = open('sample_input.txt', 'r')
  readline = sys.stdin.readline

  N = int(readline().strip())
  arr = sorted(list(map(int, readline().strip().split(" ", N)[:N])))

  print(len([i for i, _ in enumerate(arr) if is_good_number(i, arr)]))


