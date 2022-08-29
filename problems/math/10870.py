import math
from sys import stdin

new_input = stdin.readline


class Matrix:

    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def __mul__(self, other):
        return Matrix(
            self.a * other.a + self.b * other.b, self.a * other.b + self.b * other.d,
            self.c * other.a + self.d * other.c, self.c * other.b + self.d * other.d)

    def __pow__(self, other):
        log2_n = 0
        while 2 ** log2_n < other:
            log2_n += 1

        cache = [Matrix.identity(), self]

        for i in range(2, len(cache)):
            cache.append(cache[i - 1] * cache[i - 1])

        n = other

        answer = cache[0]
        for i in range(1, len(cache)):
            if n % 2 == 1:
                answer = answer * cache[i]

            n /= 2

        return answer

    @staticmethod
    def identity():
        return Matrix(1, 0, 0, 1)

    def print(self):
        print(f"{self.a} {self.b}")
        print(f"{self.c} {self.d}")


def get_answer(n):
    if n <= 0:
        return 0
    n -= 1

    depth = 1

    matrix = Matrix.identity()
    while n > 0:
        if n % 2 == 1:
            matrix = matrix * dp[depth]

        n //= 2
        depth += 1

    return matrix.a


dp = [Matrix.identity(), Matrix(1, 1, 1, 0)]

if __name__ == '__main__':
    n = int(new_input())

    max_input = 19

    log2_n = 0
    while 2 ** log2_n <= max_input:
        log2_n += 1

    for i in range(2, log2_n + 1):
        dp.append(dp[i - 1] * dp[i - 1])

    print(get_answer(n))

