# 배낭 문제 (Knapsack Problem)

> 구현: [`knapsack.py`](./knapsack.py) — `knapsack()`, `knapsackWithOneOrZero()`, `knapsackWithSufficientStock()`
> 관련 테스트: [`tests/knapsack/test_knapsack.py`](../../tests/knapsack/test_knapsack.py)

## 1. 왜 이 알고리즘이 필요한가?

배낭 문제는 이름 그대로입니다: 무게 한도가 정해진 배낭에, 각각 무게와 가치가 다른 물건들을 넣어서 **가치의 합이 최대가 되도록** 고르는 문제입니다. 등산 배낭을 쌀 때 "이 물 한 병(무거움, 생존에 중요) vs 이 카메라(가벼움, 있으면 좋음)" 사이에서 고민하는 것과 똑같습니다.

이 문제가 흥미로운 이유는, 얼핏 "그냥 가치 높은 순서로 넣으면 되지 않나?" 싶지만 그렇지 않다는 데 있습니다. 가치가 높아도 무게가 너무 무거워서 오히려 가벼운 물건 여러 개를 넣는 게 나을 수도 있습니다. 물건 개수가 `n`개일 때 "넣는다/안 넣는다"의 모든 조합은 `2^n`가지이므로, 완전탐색(brute force)으로 전부 따져보면 물건이 20개만 넘어가도 100만 가지가 넘는 조합을 검사해야 합니다.

**동적계획법(DP)은 이 완전탐색에서 중복되는 계산을 딱 한 번만 하도록 재활용해서, `O(물건 수 × 배낭 용량)`이라는 훨씬 빠른 시간에 답을 구합니다.**

## 2. 두 가지 변형: 0/1 배낭 vs 무한 배낭

`knapsack.py`는 두 가지 문제를 하나의 진입점으로 제공합니다.

```python
def knapsack(weights, values, max_weight, one_or_zero=False):   # knapsack.py:1
    if one_or_zero:
        return knapsackWithOneOrZero(weights, values, max_weight)      # knapsack.py:6 — 0/1 배낭
    else:
        return knapsackWithSufficientStock(weights, values, max_weight)  # knapsack.py:8 — 무한 배낭
```

| 옵션 | 의미 | 비유 |
|---|---|---|
| `one_or_zero=True` | **0/1 배낭**: 각 물건을 최대 1개까지만 넣을 수 있음 | 등산 배낭 — 카메라는 하나뿐 |
| `one_or_zero=False` (기본값) | **무한(unbounded) 배낭**: 같은 물건을 몇 개든 반복해서 넣을 수 있음 | 마트에서 물건 골라 담기 — 같은 상품 여러 개 살 수 있음 |

`test_cannot_take_item_twice`(`test_knapsack.py:17`)와 `test_reuses_best_item_to_fill_capacity`(`test_knapsack.py:33`)가 이 둘의 차이를 정확히 보여줍니다: 무게 5, 가치 10인 물건 하나로 용량 23짜리 배낭을 채우면, 0/1 배낭은 `10`(딱 한 번만 넣을 수 있으므로)인 반면 무한 배낭은 `40`(5짜리를 4번 넣어 무게 20, 남는 용량 3은 못 씀)이 나옵니다.

## 3. DP 점화식과 테이블 — 0/1 배낭

`weights = [2, 3, 4, 5]`, `values = [3, 4, 5, 6]`, `max_weight = 5`인 예시(`test_classic_example`, `test_knapsack.py:8`)로 살펴봅시다. 기대값은 `7`입니다.

점화식은 다음과 같습니다. `dp[i][w]`를 "물건을 `i`번째까지 고려했을 때, 무게 한도 `w` 안에서 얻을 수 있는 최대 가치"라고 정의하면:

```
dp[i][w] = dp[i-1][w]                              (i번째 물건을 안 넣는 경우)
dp[i][w] = max(dp[i-1][w], dp[i-1][w - weight_i] + value_i)   (넣을 수 있다면, 넣는 경우와 비교)
```

즉 "이 물건을 넣을까 말까"를 결정할 때, **바로 이전 단계(i-1)의 결과만 있으면 충분**합니다. 이 테이블을 직접 채워보면:

```
              w=0   w=1   w=2   w=3   w=4   w=5
아무것도 안 넣음   0     0     0     0     0     0
+물건1(w2,v3)     0     0     3     3     3     3
+물건2(w3,v4)     0     0     3     4     4     7
+물건3(w4,v5)     0     0     3     4     5     7
+물건4(w5,v6)     0     0     3     4     5     7
                                                 ↑
                                        dp[전체][5] = 7  ✓
```

예를 들어 `w=5`행에서 물건2(무게3,가치4)를 추가할 때: `dp[물건1][5]=3`(안 넣음) vs `dp[물건1][5-3=2]+4 = 3+4 = 7`(넣음) 중 큰 값인 `7`을 선택합니다. 이 `7`(물건1+물건2 = 무게 5, 가치 3+4=7)이 최종 정답과 같습니다.

## 4. `knapsackWithOneOrZero()` — 배열 두 개로 테이블을 압축

`knapsackWithOneOrZero()`(`knapsack.py:26`)는 위 2차원 테이블을 통째로 저장하지 않고, **직전 행(before_dp)과 현재 행(after_dp)** 두 줄짜리 배열만 유지합니다.

```python
def knapsackWithOneOrZero(weights, values, max_weight):
    before_dp = [0] * (max_weight + 1)     # knapsack.py:30
    after_dp = [0] * (max_weight + 1)      # knapsack.py:31

    for weight, value in zip(weights, values):     # knapsack.py:33 — 물건을 하나씩 처리
        for w in range(max_weight, -1, -1):          # knapsack.py:34 — 용량을 "큰 값부터" 훑음
            if w < weight:
                after_dp[w] = before_dp[w]              # knapsack.py:36 — 못 넣음 → 이전 값 그대로
            else:
                after_dp[w] = max(before_dp[w], before_dp[w - weight] + value)   # knapsack.py:38

        before_dp, after_dp = after_dp, before_dp    # knapsack.py:40 — 행 교체(다음 물건을 위해)

    return before_dp[max_weight]     # knapsack.py:42
```

여기서 핵심은 `after_dp[w]`를 계산할 때 항상 `before_dp`(직전 물건까지의 결과)만 참조한다는 점입니다. 같은 물건을 두 번 세는 일이 없도록, "이번 물건을 고려하기 전" 상태와 "고려한 후" 상태를 철저히 분리합니다. 이는 흔히 쓰이는 "하나의 배열을 뒤에서부터 갱신"하는 최적화(`for w in range(max_weight, 0, -1)`)와 원리상 동일하며, 이 구현은 그 대신 두 개의 배열을 번갈아 사용하는 방식을 택했습니다.

## 5. `knapsackWithSufficientStock()` — 같은 물건을 여러 번 쓸 수 있다면?

```python
def knapsackWithSufficientStock(weights, values, max_weight):
    dp = [0] * (max_weight + 1)                # knapsack.py:16

    for weight, value in zip(weights, values):   # knapsack.py:18
        for w in range(0, max_weight + 1):         # knapsack.py:19 — 용량을 "작은 값부터" 훑음
            if w >= weight:
                dp[w] = max(dp[w], dp[w - weight] + value)   # knapsack.py:21

    return dp[max_weight]      # knapsack.py:23
```

0/1 배낭과 코드는 거의 비슷해 보이지만 결정적인 차이가 하나 있습니다: **배열을 하나만 쓰고, `w`를 작은 값부터 큰 값으로(오름차순) 갱신**합니다. 이렇게 하면 `dp[w - weight]`를 참조할 때 이미 **이번 물건으로 갱신된 값**을 읽게 되므로, 같은 물건을 여러 번 사용한 효과가 자연스럽게 누적됩니다.

`weights = [1, 3, 4, 5]`, `values = [1, 4, 5, 7]`, `max_weight = 7`(`test_classic_example`, `test_knapsack.py:42`, 기대값 `9`)로 배열이 채워지는 과정:

```
              w=0  w=1  w=2  w=3  w=4  w=5  w=6  w=7
초기값          0    0    0    0    0    0    0    0
+물건(w1,v1)    0    1    2    3    4    5    6    7   ← 1짜리를 계속 재사용 가능
+물건(w3,v4)    0    1    2    4    5    6    8    9   ← dp[7] = dp[4]+4 = 5+4 = 9
+물건(w4,v5)    0    1    2    4    5    6    8    9   ← 갱신 없음 (기존 값이 이미 더 큼)
+물건(w5,v7)    0    1    2    4    5    7    8    9   ← dp[5] = dp[0]+7 = 0+7 = 7 로 갱신

dp[7] = 9  ✓
```

`w`를 **거꾸로(큰 값부터)** 갱신하면 0/1 배낭이 되고, **정방향(작은 값부터)** 갱신하면 무한 배낭이 된다 — 이 한 방향 차이가 두 문제를 가르는 전부입니다.

## 6. 완전탐색 대비 DP가 빠른 이유

| | 완전탐색 (Brute Force) | 동적계획법 (DP) |
|---|---|---|
| 접근 방식 | 물건마다 "넣는다/안 넣는다"를 전부 시도 | `dp[w]`라는 표에 부분 문제의 답을 저장하고 재사용 |
| 시간복잡도 | `O(2^n)` | `O(n × max_weight)` |
| 왜 느린가/빠른가 | 같은 "부분 배낭 채우기" 문제를 몇 번이고 처음부터 다시 계산 | 동일한 `(물건 번호, 남은 용량)` 조합은 값이 항상 같다는 점(**최적 부분 구조**)을 이용해, 한 번 계산한 값을 표에 저장해두고 **중복 계산을 없앰**(**중복 부분 문제**) |

DP가 성립하는 이유는 두 가지 성질 덕분입니다.

- **최적 부분 구조(Optimal Substructure)**: "물건 `i`개, 용량 `w`"의 최적해는 "물건 `i-1`개, 용량 `w`(또는 `w-weight`)"의 최적해로부터 구성될 수 있습니다. 즉 부분 문제의 최적해를 조합하면 전체 문제의 최적해가 됩니다.
- **중복 부분 문제(Overlapping Subproblems)**: 완전탐색으로 재귀를 돌리면 `(물건 번호, 남은 용량)`이 같은 상태를 몇 번이고 다시 계산하게 됩니다. DP는 이 상태를 배열(`dp[w]`)에 저장해 두었다가 재사용하므로, 상태 하나당 계산은 딱 한 번만 이루어집니다.

## 7. 시간복잡도 / 공간복잡도

| 구현 | 시간복잡도 | 공간복잡도 |
|---|---|---|
| `knapsackWithSufficientStock` (무한 배낭) | `O(n × W)` | `O(W)` |
| `knapsackWithOneOrZero` (0/1 배낭) | `O(n × W)` | `O(W)` (배열 2개) |
| 완전탐색 (0/1 배낭) | `O(2^n)` | `O(n)` (재귀 스택) |

(`n` = 물건 개수, `W` = `max_weight`)

## 8. 개념 ↔ 코드 대응표

| 개념 | 코드 위치 |
|---|---|
| 0/1 배낭과 무한 배낭을 하나의 진입점으로 분기 | `knapsack()` (`knapsack.py:1-8`) |
| 무한 배낭 DP (같은 물건 재사용 가능) | `knapsackWithSufficientStock()` (`knapsack.py:11-23`) |
| DP 점화식 — 정방향(오름차순) 갱신 | `for w in range(0, max_weight + 1)` (`knapsack.py:19`) |
| 0/1 배낭 DP (물건마다 최대 1개) | `knapsackWithOneOrZero()` (`knapsack.py:26-42`) |
| DP 점화식 — 역방향(내림차순) 갱신으로 중복 사용 방지 | `for w in range(max_weight, -1, -1)` (`knapsack.py:34`) |
| 이전 행/현재 행을 배열 두 개로 표현 | `before_dp`, `after_dp` (`knapsack.py:30-31`, 교체는 `knapsack.py:40`) |
| 입력 검증 (길이 불일치, 음수 용량) | `assert` 문들 (`knapsack.py:2-3`, `12-13`, `27-28`) |

## 9. 직접 실행해보기

이 파일에는 `if __name__ == '__main__':` 데모 블록이 없으므로, 함수를 바로 호출해서 확인합니다.

```bash
python3 -c "
from algorithm.knapsack.knapsack import knapsack
weights, values = [2, 3, 4, 5], [3, 4, 5, 6]
print('0/1 knapsack:', knapsack(weights, values, 5, one_or_zero=True))
print('unbounded  :', knapsack(weights, values, 5, one_or_zero=False))
"
```

```bash
pytest tests/knapsack/test_knapsack.py -v
```

---

이전 문서: [← 오일러 피 함수](../euclidean/README.md) | 다음 문서: [백트래킹 →](../backtracking/README.md)
