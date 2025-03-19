class Solution:
  def missing_number(self, nums: list[int]) -> int:
    nums_set = set(nums)

    return [i for i in range(len(nums) + 2) if i not in nums_set][0]


if __name__ == '__main__':
  assert Solution().missing_number([0, 2, 3]) == 1