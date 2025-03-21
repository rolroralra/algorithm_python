class Solution:
  def __init__(self):
    self.__pretty_primes = [2, 3, 5]

  def is_ugly(self, n: int) -> bool:
    if n <= 0:
      return False

    for prime in self.__pretty_primes:
      while n % prime == 0:
        n //= prime

    return n == 1


if __name__ == '__main__':
  solution = Solution()

  assert solution.is_ugly(6) == True
  assert solution.is_ugly(7) == False
  assert solution.is_ugly(1) == True
  assert solution.is_ugly(14) == False
  assert solution.is_ugly(8) == True
  assert solution.is_ugly(26) == False
  assert solution.is_ugly(15) == True
