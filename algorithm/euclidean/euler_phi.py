import math

class EulerPhi:
    __slots__ = ['max_number', 'phi_values']

    def __init__(self):
        self.max_number = None
        self.phi_values = None


    def init(self, N):
        self.max_number = N
        self.phi_values = [i for i in range(0, N + 1)]

        for i in range(2, N + 1):
            if self.phi_values[i] == i:
                for j in range(i, N + 1, i):
                    self.phi_values[j] -= self.phi_values[j] // i

        print(f"{self.phi_values}")


    def __call__(self, n):
        if not self.max_number or n > self.max_number:
            self.init(n)

        return self.phi_values[n]


    def __phi__(self, n):
        if n != self.max_number:
            self.init(n)

        return self.phi_values[n]


    def phi_by_factorization(self, N):
        result = N
        n = N

        for i in range(2, math.isqrt(N) + 1):
            if n % i == 0:
                result -= result // i
                while n % i == 0:
                    n //= i

        # 여기서 남은 n은 오직 하나의 소인수일 수밖에 없다
        # √n 이하의 모든 소인수는 위 루프에서 제거됨
        # 루프가 끝났는데 n > 1 이면,
        #   → 그 n은 √n보다 큰 소수이며
        #   → 복수의 인수가 남을 수 없음 (그 중 하나는 √n 이하여야 하므로 루프에서 제거됐어야 함)
        if n > 1:
            result -= result // n

        return result


phi = EulerPhi()

print(phi(45))
print(phi.phi_by_factorization(45))
