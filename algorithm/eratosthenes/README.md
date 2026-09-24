# 에라토스테네스의 체 (Sieve of Eratosthenes)

> 구현: [`erathosthenes_sieve.py`](./erathosthenes_sieve.py) — `eratosthenes_sieve()`, `is_prime()`
> 관련 테스트: [`tests/eratosthenes/test_erathosthenes_sieve.py`](../../tests/eratosthenes/test_erathosthenes_sieve.py)

## 1. 왜 이 알고리즘이 필요한가?

"1부터 100만 사이의 소수를 모두 구하라"는 문제를 생각해봅시다. 가장 단순한 방법은 각 숫자마다 "이 수가 소수인가?"를 하나씩 물어보는 것입니다 — 이 파일의 `is_prime()`이 바로 그 방식입니다. 숫자 하나를 판별하는 데 `O(√n)`이 걸리므로, `n`개의 숫자를 전부 검사하면 `O(n√n)`이나 걸립니다.

그런데 실제로는 "숫자 하나가 소수인지"보다 "특정 범위 안의 소수를 전부 나열하라"는 요구가 훨씬 흔합니다. 이럴 땐 숫자 하나하나를 독립적으로 판별하는 대신, **처음부터 끝까지 한 번에 걸러내는 체(sieve)를 사용하는 것**이 훨씬 빠릅니다.

비유하자면, 콩 속에서 돌을 골라낼 때 콩알 하나하나를 손으로 집어서 "이게 돌인가?"를 확인하는 대신, 구멍 뚫린 체에 와르르 쏟아부어서 걸러내는 것과 같습니다. 소수가 아닌 수(합성수)는 반드시 더 작은 소수의 배수이므로, "이미 찾은 소수의 배수를 전부 지워버리면" 남는 수는 자동으로 소수가 됩니다. 이 방식이 바로 기원전 그리스 수학자 에라토스테네스(Eratosthenes)가 고안한 "체(sieve)"이고, 전체를 `O(n log log n)`에 처리할 수 있습니다.

## 2. 핵심 아이디어: 소수의 배수를 전부 지운다

1부터 N까지의 수를 모두 "소수(True)"라고 가정한 배열에서 시작합니다. 그리고 2부터 순서대로 훑으면서, 아직 지워지지 않은(=소수로 남아있는) 수를 만나면 그 수의 배수를 전부 지웁니다.

```
N = 30 이라고 하면...

시작:  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30
       모두 "소수"로 가정 (True)

i=2 (소수) → 4, 6, 8, 10, ... 지우기(X)
       2  3  X  5  X  7  X  9  X 11  X 13  X 15  X 17  X 19  X 21  X 23  X 25  X 27  X 29  X

i=3 (아직 안 지워짐 → 소수) → 9, 12, 15, ... 지우기
       2  3  X  5  X  7  X  X  X 11  X 13  X  X  X 17  X 19  X  X  X 23  X 25  X  X  X 29  X

i=4 → 이미 지워짐(합성수) → 건너뜀 (아무것도 하지 않음)

i=5 (아직 안 지워짐 → 소수) → 25 지우기 (10, 15, 20은 이미 지워짐)
       2  3  X  5  X  7  X  X  X 11  X 13  X  X  X 17  X 19  X  X  X 23  X  X  X  X  X 29  X

결과: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29
```

## 3. 왜 `√n`까지만 확인해도 충분한가?

`erathosthenes_sieve.py:9`를 보면 바깥 루프가 `math.isqrt(max_number)`, 즉 `√N`까지만 돕니다.

```python
for i in range(2, math.isqrt(max_number) + 1):   # erathosthenes_sieve.py:9
```

이게 가능한 이유는 간단합니다: **합성수 `n`은 항상 `√n` 이하인 소인수를 하나는 가지고 있기 때문**입니다.

```
합성수 n = p × q  (p ≤ q 라고 가정)

만약 p 와 q 가 둘 다 √n 보다 크다면?
  → p × q > √n × √n = n   (모순! n = p×q 인데 n 보다 커짐)

따라서 p ≤ q 인 두 인수 중 "작은 쪽" p는 반드시 √n 이하여야 한다.
```

즉 `N` 이하의 모든 합성수는, `√N` 이하의 어떤 소수의 배수로 반드시 한 번은 걸러집니다. 그래서 `i`가 `√N`을 넘어가면 더 이상 새로 지울 게 없습니다 — 이미 다 지워진 상태입니다.

같은 이유로 안쪽 루프도 `i`부터가 아니라 **`i * i`부터** 시작합니다(`erathosthenes_sieve.py:13`).

```python
for j in range(i * i, max_number + 1, i):   # erathosthenes_sieve.py:13
```

`i`의 배수 중 `2i, 3i, ..., (i-1)i`는 각각 `2, 3, ..., (i-1)`이라는 **더 작은 수의 배수이기도 하므로 이미 그 수들을 처리할 때 지워졌습니다.** 예를 들어 `i=5`일 때 `10=2×5`와 `15=3×5`는 이미 `i=2`, `i=3` 단계에서 지워졌으므로, `5`부터가 아니라 `25=5×5`부터 지우기 시작해도 됩니다. 이 최적화 덕분에 불필요한 중복 작업을 줄일 수 있습니다.

## 4. 코드 흐름

```python
def eratosthenes_sieve(max_number=100):
    is_prime = [True] * (max_number + 1)      # erathosthenes_sieve.py:4  — 일단 전부 소수로 가정

    is_prime[0] = False                        # erathosthenes_sieve.py:6  — 0, 1은 소수가 아님
    is_prime[1] = False                        # erathosthenes_sieve.py:7

    for i in range(2, math.isqrt(max_number) + 1):   # erathosthenes_sieve.py:9
        if not is_prime[i]:                     # erathosthenes_sieve.py:10 — 이미 지워졌으면(합성수) 건너뜀
            continue

        for j in range(i * i, max_number + 1, i):    # erathosthenes_sieve.py:13
            is_prime[j] = False                 # erathosthenes_sieve.py:14 — i의 배수를 전부 지움

    return [number for number, is_prime in enumerate(is_prime) if is_prime]   # erathosthenes_sieve.py:16
```

마지막 줄(`erathosthenes_sieve.py:16`)에서는 `True`로 남아있는(=끝까지 지워지지 않은) 인덱스만 모아서 반환합니다. 참고로 이 리스트 컴프리헨션 안에서 `is_prime`이라는 이름이 다시 등장하는데, 이건 컴프리헨션의 지역 변수일 뿐 바깥의 `is_prime` 배열이나 모듈 하단의 `is_prime()` 함수(19번째 줄)와는 별개입니다 — 파이썬의 컴프리헨션은 자신만의 스코프를 가지기 때문에 이름이 겹쳐도 충돌하지 않습니다.

## 5. `is_prime()`과의 차이 — "여러 개 vs 하나"

같은 파일에 있는 `is_prime(number)`(`erathosthenes_sieve.py:19`)는 완전히 다른 접근입니다.

```python
def is_prime(number):
    if number < 2:
        return False

    return all(number % i != 0 for i in range(2, math.isqrt(number) + 1))
```

이 함수는 숫자 **하나**를 받아서, `2`부터 `√number`까지 나누어떨어지는 값이 있는지 시행착오(trial division)로 확인합니다. 매번 `O(√n)`이 걸립니다.

| | `eratosthenes_sieve(N)` | `is_prime(n)` |
|---|---|---|
| 용도 | 1~N 사이 **모든** 소수 나열 | **하나의** 숫자가 소수인지 판별 |
| 시간복잡도 | `O(N log log N)` (전체 한 번) | `O(√n)` (호출마다) |
| N개를 전부 알고 싶다면 | `O(N log log N)` | `O(N√N)` (숫자마다 반복 호출) |

즉 "범위 안의 소수를 다 알고 싶다"면 체가 압도적으로 유리하고, "이 숫자 하나만 궁금하다"면 `is_prime()`처럼 그때그때 판별하는 게 더 간단합니다. `test_matches_sieve_for_range`(`test_erathosthenes_sieve.py:42`)는 두 함수가 항상 같은 결과를 내는지 0~199 전체 범위에서 교차 검증합니다.

## 6. 시간복잡도 / 공간복잡도

| 알고리즘 | 시간복잡도 | 공간복잡도 |
|---|---|---|
| `eratosthenes_sieve(N)` | `O(N log log N)` | `O(N)` (`is_prime` 불리언 배열) |
| `is_prime(n)` (단일 판별) | `O(√n)` | `O(1)` |
| 단순 시행착오로 1~N 모두 판별 | `O(N√N)` | `O(1)` |

`O(N log log N)`이 되는 이유는, 각 소수 `p`마다 배수를 지우는 데 대략 `N/p`번의 연산이 필요하고, 이를 모든 소수에 대해 합하면 `N × (1/2 + 1/3 + 1/5 + 1/7 + ...)`가 되는데, 소수의 역수의 합은 `log log N`에 가깝게 수렴한다는 정수론 결과(메르텐스 정리) 때문입니다. `log log N`은 N이 아무리 커져도 매우 천천히 자라므로, 사실상 `O(N)`에 가까운 성능이라고 볼 수 있습니다.

## 7. 개념 ↔ 코드 대응표

| 개념 | 코드 위치 |
|---|---|
| "일단 전부 소수로 가정"하는 불리언 배열 | `is_prime = [True] * (max_number + 1)` (`erathosthenes_sieve.py:4`) |
| 0, 1은 소수가 아니라는 예외 처리 | `erathosthenes_sieve.py:6-7` |
| `√N`까지만 확인해도 충분한 이유 구현 | `range(2, math.isqrt(max_number) + 1)` (`erathosthenes_sieve.py:9`) |
| 이미 걸러진 합성수는 건너뛰기 | `if not is_prime[i]: continue` (`erathosthenes_sieve.py:10-11`) |
| `i`의 배수를 `i*i`부터 지우는 최적화 | `range(i * i, max_number + 1, i)` (`erathosthenes_sieve.py:13`) |
| 결과 수집 (남은 소수만 추리기) | `erathosthenes_sieve.py:16` |
| 숫자 하나만 판별하는 시행착오 방식 | `is_prime()` (`erathosthenes_sieve.py:19`) |

## 8. 직접 실행해보기

이 파일에는 별도의 `if __name__ == '__main__':` 데모 블록은 없지만, 함수를 바로 임포트해서 결과를 확인할 수 있습니다.

```bash
python3 -c "from algorithm.eratosthenes.erathosthenes_sieve import eratosthenes_sieve, is_prime; \
print(eratosthenes_sieve(50)); \
print(is_prime(97), is_prime(100))"
```

테스트를 직접 돌려보면 체 방식과 시행착오 방식이 항상 같은 결과를 내는지 확인할 수 있습니다.

```bash
pytest tests/eratosthenes/test_erathosthenes_sieve.py -v
```

---

이전 문서 없음 (알고리즘 시리즈의 첫 문서입니다) | 다음 문서: [오일러 피 함수 →](../euclidean/README.md)
