class Solution:
  def add_digits(self, num: int) -> int:
    result = sum(int(c) for c in str(num))

    if (result < 10):
      return result

    return self.add_digits(result)

if __name__ == '__main__':
  assert Solution().add_digits(38) == 2
