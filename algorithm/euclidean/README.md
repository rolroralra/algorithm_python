# 오일러 피 함수 (Euler's Totient Function, φ(n))

> 구현: [`euler_phi.py`](./euler_phi.py) — `EulerPhi` 클래스
> 관련 테스트: [`tests/euclidean/test_euler_phi.py`](../../tests/euclidean/test_euler_phi.py)
> 이 문서를 읽기 전에 [`../eratosthenes/README.md`](../eratosthenes/README.md)의 "체(sieve)" 개념을 먼저 알고 있으면 이해가 쉽습니다 — 이 파일의 `init()`도 같은 방식으로 동작합니다.

> **디렉토리 이름에 대한 참고**: 이 폴더 이름은 `euclidean`이지만, 실제로 파일 안에 유클리드 호제법(GCD를 구하는 그 알고리즘) 코드는 없습니다. `gcd()` 함수도, 나머지 연산을 반복하는 호제법 루프도 존재하지 않습니다. 아래에서 다시 설명하지만, 유클리드 호제법은 이 파일에서 **"서로소(coprime)"라는 개념을 정의하는 배경 이론**으로만 연결되어 있을 뿐, 실제 계산은 체(sieve)와 소인수분해 두 가지 방식으로 이루어집니다.

## 1. 왜 이 함수가 필요한가?

암호학(RSA 등)이나 정수론 문제를 풀다 보면 "1부터 n까지의 수 중에서, n과 공약수가 1밖에 없는(=서로소인) 수가 몇 개나 될까?"라는 질문을 자주 만납니다. 이 개수를 세는 함수가 바로 **오일러 피 함수 φ(n)**입니다.

예를 들어 `n = 45`(= 3² × 5)일 때, 1~45 중 3의 배수도 아니고 5의 배수도 아닌 수의 개수를 세면 24개가 나옵니다 — 이 값이 바로 `φ(45) = 24`입니다.

```
두 수 a, n이 "서로소(coprime)"라는 것은 gcd(a, n) = 1 이라는 뜻입니다.
gcd(a, n)을 구하는 가장 대표적인 방법이 유클리드 호제법(Euclidean algorithm)입니다.

φ(n) = "1 이상 n 이하의 정수 중 gcd(k, n) = 1을 만족하는 k의 개수"
```

즉 φ(n)의 **정의 자체**는 유클리드 호제법이 계산하는 gcd와 맞닿아 있습니다. 하지만 1부터 n까지 매번 `gcd(k, n)`을 계산해서 세는 방식은 `n`번의 호제법 호출이 필요해 비효율적입니다(대략 `O(n log n)`). 이 파일의 `EulerPhi` 클래스는 그보다 훨씬 빠른 두 가지 방법 — **체 기반 계산**과 **소인수분해 공식** — 을 제공합니다.

## 2. 핵심 공식: 소인수분해로 φ(n) 구하기

φ(n)은 다음 공식으로 구할 수 있습니다(오일러의 곱셈 공식).

```
n = p1^a1 × p2^a2 × ... × pk^ak  (서로 다른 소인수들로 분해했을 때)

φ(n) = n × (1 - 1/p1) × (1 - 1/p2) × ... × (1 - 1/pk)
```

예를 들어 `45 = 3² × 5`이므로:

```
φ(45) = 45 × (1 - 1/3) × (1 - 1/5)
      = 45 × (2/3) × (4/5)
      = 45 × 8/15
      = 24
```

이 공식이 직관적으로 성립하는 이유는 "포함-배제 원리"입니다: 전체 `n`개 중에서 소인수 `p1`의 배수(`n/p1`개)를 빼고, `p2`의 배수(`n/p2`개)를 빼되, 둘 다의 배수(`n/(p1p2)`개)를 다시 더해주는 식으로 정리하면 위 곱셈 형태로 깔끔하게 떨어집니다.

## 3. 방법 1 — 체(sieve) 기반 계산: `init()` / `__call__()`

`init()`(`euler_phi.py:11`)은 1~N까지 **모든** φ 값을 한 번에 미리 계산해두는 방식입니다. [에라토스테네스의 체](../eratosthenes/README.md)와 원리가 거의 같습니다 — 소수를 하나 찾을 때마다 그 소수와 관련된 모든 배수를 한꺼번에 갱신합니다.

```python
def init(self, N):
    self.max_number = N
    self.phi_values = [i for i in range(0, N + 1)]     # euler_phi.py:13 — 일단 phi_values[i] = i로 초기화

    for i in range(2, N + 1):                            # euler_phi.py:15
        if self.phi_values[i] == i:                       # euler_phi.py:16 — 아직 아무도 안 건드렸다 = i는 소수
            for j in range(i, N + 1, i):                   # euler_phi.py:17 — i의 배수 j마다
                self.phi_values[j] -= self.phi_values[j] // i   # euler_phi.py:18 — (1 - 1/i) 배 적용
```

동작 원리를 뜯어보면:

1. `phi_values`를 처음엔 `[0, 1, 2, 3, ..., N]`으로, 즉 자기 자신 값으로 채웁니다.
2. `i`를 2부터 N까지 훑으면서, **`phi_values[i]`가 아직 `i` 그대로라면** — 이는 지금까지 어떤 소인수도 이 값을 건드리지 않았다는 뜻이므로, `i`는 소수입니다(에라토스테네스의 체와 똑같은 "아직 지워지지 않았다 = 소수" 판정법).
3. `i`가 소수로 확인되면, `i`의 모든 배수 `j`에 대해 `phi_values[j] -= phi_values[j] // i`를 적용합니다. 이는 `phi_values[j]`에 `(1 - 1/i)`를 곱하는 것과 같습니다(`x - x/i = x × (1 - 1/i)`). `j`가 가진 서로 다른 소인수 각각에 대해 이 과정이 한 번씩 일어나므로, 최종적으로 오일러의 곱셈 공식이 그대로 누적됩니다.

`45`를 예로 들면:

```
초기값:            phi_values[45] = 45

i=3 (소수, 3 | 45)  →  phi_values[45] -= 45 // 3 = 15   →  45 - 15 = 30
i=5 (소수, 5 | 45)  →  phi_values[45] -= 30 // 5 =  6   →  30 -  6 = 24

φ(45) = 24  ✓  (공식대로 45 × 2/3 × 4/5 = 24 와 일치)
```

`__call__()`(`euler_phi.py:23`)은 이렇게 만든 표를 캐시처럼 재사용합니다.

```python
def __call__(self, n):
    if not self.max_number or n > self.max_number:   # euler_phi.py:24
        self.init(n)

    return self.phi_values[n]                          # euler_phi.py:27
```

한 번 `init(N)`을 해두면, `n ≤ N`인 모든 조회는 표를 다시 만들지 않고 `O(1)`로 즉시 응답합니다. 반대로 지금까지 계산해둔 범위(`max_number`)보다 큰 `n`이 들어오면 그 `n`까지 다시 전체를 계산합니다 — `test_reinitializes_when_queried_beyond_current_range`(`test_euler_phi.py:21`)가 이 동작을 검증합니다.

> **참고**: 같은 클래스에 `__phi__()`(`euler_phi.py:30`)라는 메서드도 있습니다. 이름이 이중 밑줄로 감싸여 있어 파이썬 매직 메서드처럼 보이지만, 실제로 파이썬이 자동으로 호출해주는 매직 메서드가 아니라 그냥 그렇게 이름 붙인 일반 메서드입니다. 동작도 `__call__()`과 다릅니다 — `n != self.max_number`이면 **매번** `init(n)`을 다시 실행하므로, 캐시를 재사용하지 않고 호출할 때마다 새로 표를 만듭니다. 테스트에서는 이 메서드를 사용하지 않습니다.

## 4. 방법 2 — 소인수분해 공식: `phi_by_factorization()`

`init()`이 "1~N 전체"를 한 번에 구하는 방식이라면, `phi_by_factorization(N)`(`euler_phi.py:37`)은 **딱 하나의 값**만 필요할 때 쓰는 방식입니다. 시행착오(trial division)로 소인수를 직접 찾아가며 공식을 그대로 적용합니다.

```python
def phi_by_factorization(self, N):
    result = N
    n = N

    for i in range(2, math.isqrt(N) + 1):     # euler_phi.py:41 — √N까지만 확인 (에라토스테네스와 같은 이유)
        if n % i == 0:                          # euler_phi.py:42 — i가 소인수라면
            result -= result // i                # euler_phi.py:43 — (1 - 1/i) 적용
            while n % i == 0:                     # euler_phi.py:44 — i로 계속 나눠서 다음 소인수 탐색 준비
                n //= i

    if n > 1:                                  # euler_phi.py:52 — √N보다 큰 소인수가 하나 남아있다면
        result -= result // n                    # euler_phi.py:53
```

`N = 45`로 따라가 보면:

```
result = 45, n = 45   (isqrt(45) = 6 이므로 i는 2~6까지 확인)

i = 2: 45 % 2 != 0 → 건너뜀
i = 3: 45 % 3 == 0 → result -= 45 // 3 = 15  →  result = 30
                     n을 3으로 계속 나눔: 45 → 15 → 5  (더 이상 3으로 안 나눠짐, n = 5)
i = 4: 5 % 4 != 0 → 건너뜀
i = 5: 5 % 5 == 0 → result -= 30 // 5 = 6  →  result = 24
                     n을 5로 나눔: 5 → 1  (n = 1)
i = 6: 1 % 6 != 0 → 건너뜀
루프 종료 후 n = 1 이므로 마지막 if(n > 1)는 실행되지 않음

φ(45) = 24  ✓
```

코드 주석(`euler_phi.py:47-51`)이 설명하듯, 루프가 `√N`까지만 돌아도 안전한 이유는 소인수분해의 성질 때문입니다: 만약 루프가 끝난 뒤에도 `n > 1`이 남아있다면, 그 `n`은 `√N`보다 큰 소수 하나일 수밖에 없습니다(둘 이상의 인수가 남으려면 그중 하나는 반드시 `√N` 이하여야 하고, 그랬다면 이미 루프에서 걸러졌을 것이기 때문입니다). 그래서 마지막에 `if n > 1`로 그 하나 남은 소인수를 한 번 더 처리해줍니다.

## 5. 두 방법 비교

| | `init()` + `__call__()` (체) | `phi_by_factorization()` (소인수분해) |
|---|---|---|
| 용도 | 1~N 범위의 φ 값을 **여러 번** 조회 | φ(n) 값을 **한 번만** 필요할 때 |
| 최초 계산 비용 | `O(N log log N)` (범위 전체) | `O(√N)` (그 값 하나만) |
| 재조회 비용 | `O(1)` (캐시된 표 재사용) | 매번 다시 `O(√N)` |
| N개를 전부 구해야 한다면 | `O(N log log N)` | `O(N√N)` |

`test_matches_sieve_based_computation`(`test_euler_phi.py:39-41`)은 2~99 전체 범위에서 두 방식이 항상 같은 값을 내는지 교차 검증합니다.

## 6. 개념 ↔ 코드 대응표

| 개념 | 코드 위치 |
|---|---|
| φ 값 캐시 테이블 | `EulerPhi.phi_values` (`euler_phi.py:4`, `euler_phi.py:13`) |
| 체 방식으로 1~N 전체 φ 값 계산 | `init()` (`euler_phi.py:11-20`) |
| "아직 안 건드려졌다 = 소수" 판정 | `if self.phi_values[i] == i` (`euler_phi.py:16`) |
| `(1 - 1/i)` 배 적용 (오일러 곱셈 공식) | `phi_values[j] -= phi_values[j] // i` (`euler_phi.py:18`) |
| 캐시를 활용한 조회 (범위 밖이면 재계산) | `__call__()` (`euler_phi.py:23-27`) |
| 매번 재계산하는 대안 구현 (테스트되지 않음) | `__phi__()` (`euler_phi.py:30-34`) |
| 소인수분해로 φ(n) 하나만 계산 | `phi_by_factorization()` (`euler_phi.py:37-55`) |
| `√N`까지만 검사해도 되는 이유 | `euler_phi.py:47-51` 주석 |

## 7. 직접 실행해보기

이 파일은 `if __name__ == '__main__':` 블록 없이, **모듈 최하단에 바로** 실행 코드가 있습니다(`euler_phi.py:58-61`). 즉 이 모듈을 임포트하기만 해도 아래 코드가 즉시 실행됩니다.

```python
phi = EulerPhi()

print(phi(45))
print(phi.phi_by_factorization(45))
```

그래서 파일을 직접 실행하면 됩니다.

```bash
python3 -m algorithm.euclidean.euler_phi
```

체 초기화 과정에서 `init()`이 출력하는 `phi_values` 전체 배열(`euler_phi.py:20`)과, 그 뒤로 `phi(45)`, `phi_by_factorization(45)`의 결과(둘 다 `24`)가 순서대로 출력됩니다.

```bash
pytest tests/euclidean/test_euler_phi.py -v
```

---

이전 문서: [← 에라토스테네스의 체](../eratosthenes/README.md) | 다음 문서: [배낭 문제 (0/1 Knapsack) →](../knapsack/README.md)
