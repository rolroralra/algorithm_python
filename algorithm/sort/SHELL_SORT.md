# 쉘 정렬 (Shell Sort)

> 구현: [`sorting.py`](./sorting.py) — `Sort.shell_sort()` (`sorting.py:46`)
> 이전 문서: [INSERTION_SORT.md](./INSERTION_SORT.md) · 목차: [README.md](./README.md)

## 1. 왜 이 알고리즘이 필요한가?

삽입 정렬은 "거의 정렬된 배열"에서는 빠르지만, **작은 값이 배열 맨 뒤에 있는 경우**(예: `[2, 3, 4, ..., 100, 1]`)에는 그 작은 값을 맨 앞까지 한 칸씩 옮기느라 최악의 경우와 다를 바 없이 느려집니다. 이웃끼리만 비교/swap하기 때문에 "멀리 있는 원소"를 옮기는 데 시간이 오래 걸리는 것입니다.

쉘 정렬(1959년 Donald Shell 고안)은 이 문제를 **"이웃이 아니라 멀리 떨어진 원소끼리 먼저 비교한다"** 는 아이디어로 해결합니다. 처음에는 큰 간격(gap)으로 듬성듬성 비교하며 큰 이동을 빠르게 처리하고, 점점 간격을 좁혀가며 마지막엔 간격 1(=일반 삽입 정렬)로 마무리합니다. 이렇게 하면 마지막 일반 삽입 정렬 단계에 도달했을 때는 이미 배열이 "거의 정렬된" 상태이므로 훨씬 빠르게 끝납니다.

## 2. 핵심 아이디어: 간격(gap)을 줄여가는 삽입 정렬

`gap`만큼 떨어진 원소끼리 하나의 "부분 수열(sub-list)"을 이룬다고 생각하면 됩니다. 예를 들어 원소 8개, `gap=4`일 때는 아래처럼 4개의 부분 수열이 생깁니다.

```
index:  0  1  2  3  4  5  6  7
       [●  ○  □  △  ●  ○  □  △]
        └──────gap=4──────┘

부분 수열 1 (●): index 0, 4
부분 수열 2 (○): index 1, 5
부분 수열 3 (□): index 2, 6
부분 수열 4 (△): index 3, 7
```

각 부분 수열을 독립적으로 삽입 정렬하는 것과 같은 효과를 내면서, 실제로는 하나의 루프로 모든 부분 수열을 동시에 처리합니다. `gap`을 절반씩 줄여가며(`8 → 4 → 2 → 1`) 이 과정을 반복하고, `gap == 1`이 되면 일반 삽입 정렬과 완전히 동일해집니다.

### 실행 예시

`[5, 3, 8, 1, 9]` (`size=5`)를 정렬해봅시다. 시작 `gap = size // 2 = 2`.

```
초기 (gap=2):          [5, 3, 8, 1, 9]
                         └─gap2─┘  └─gap2─┘

  index 0,2,4 그룹: 5, 8, 9 → comp(5,8)=False → 그대로
  index 1,3   그룹: 3, 1    → comp(3,1)=True  → swap

gap=2 패스 결과:        [5, 1, 8, 3, 9]

gap을 1로 줄임 (2 // 2 = 1) → 이제 일반 삽입 정렬과 동일

gap=1 패스 결과(최종):  [1, 3, 5, 8, 9]
```

큰 간격일 때 `3`과 `1`처럼 멀리 있던 값이 한 번의 swap으로 성큼 이동했다는 점에 주목하세요. 일반 삽입 정렬이었다면 `1`이 맨 앞까지 가는 데 여러 번의 이웃 swap이 필요했을 것입니다.

## 3. 코드 살펴보기

```python
@staticmethod
def shell_sort(array, comp=lambda a, b: a > b):
    size = len(array)
    gap = size // 2
    while gap > 0:
        for i in range(gap, size):
            for j in range(i, gap - 1, -gap):
                if not comp(array[j - gap], array[j]):
                    break

                array[j - gap], array[j] = array[j], array[j - gap]

        gap //= 2
```

- `gap = size // 2`(`sorting.py:48`): **간격 수열(gap sequence)** 로 "Shell's original sequence"를 사용합니다. `n/2, n/4, ..., 1` 순서로 줄어드는 가장 단순한 수열입니다.
- `while gap > 0`(`sorting.py:49`): 간격이 0이 될 때까지(즉 `gap == 1`인 패스까지 마치고 나면) 반복.
- `for i in range(gap, size)`(`sorting.py:50`): 삽입 정렬의 바깥 루프(`for i in range(1, size)`)와 같은 역할이되, 시작점이 `1`이 아니라 `gap`입니다.
- `for j in range(i, gap - 1, -gap)`(`sorting.py:51`): 삽입 정렬의 `for j in range(i, 0, -1)`에서 이동 폭을 `1` 대신 `gap`으로 바꾼 것입니다. `array[j - gap]`와 `array[j]`를 비교(`sorting.py:53`)하며, 순서가 맞으면 즉시 `break`, 아니면 `gap`만큼 떨어진 두 원소를 swap(`sorting.py:56`)하고 계속 왼쪽으로 이동합니다.
- `gap //= 2`(`sorting.py:58`): 간격을 절반으로 줄여 다음 패스로.

**삽입 정렬과 코드를 나란히 비교하면**, 쉘 정렬은 사실상 "삽입 정렬의 이동 거리를 `1`에서 `gap`으로 일반화"한 것과 같습니다. 실제로 `gap == 1`일 때 이 코드는 `insertion_sort`와 완전히 동일하게 동작합니다.

## 4. 간격 수열(Gap Sequence)이 성능을 좌우한다

이 구현은 `size // 2`씩 줄여가는 **Shell의 원래 수열(n/2, n/4, ..., 1)** 을 사용합니다. 구현이 단순하다는 장점이 있지만, 최악의 경우 시간복잡도가 `O(n²)`까지 나빠질 수 있다는 약점이 있습니다.

이후 연구자들은 더 나은 간격 수열을 제안했습니다:

| 간격 수열 | 평균/최악 시간복잡도(대략) |
|---|---|
| Shell 원래 수열 (`n/2, n/4, ..., 1`) — 이 구현체 | 최악 `O(n²)` |
| Knuth 수열 (`(3^k - 1) / 2`) | 약 `O(n^1.5)` |
| Sedgewick 수열 | 약 `O(n^1.33)` |

즉 "쉘 정렬"은 하나의 알고리즘이 아니라, **어떤 간격 수열을 쓰느냐에 따라 성능이 달라지는 알고리즘 계열**이라고 이해하는 것이 정확합니다.

## 5. 시간복잡도 / 공간복잡도 / 안정성

| 항목 | 값 | 설명 |
|---|---|---|
| 최선(Best) | `O(n log n)` | 이미 정렬된 배열이어도 모든 gap에 대해 한 번씩은 훑어야 함 |
| 평균(Average) | 간격 수열에 따라 다름 (이 구현체 기준 대략 `O(n^1.3)` 수준으로 알려짐) | |
| 최악(Worst) | `O(n²)` | 이 구현체가 쓰는 `n/2` 수열의 알려진 약점 |
| 공간(Space) | `O(1)` | in-place, swap만 사용 |
| 안정성(Stable) | ❌ 불안정 | 멀리 떨어진(gap만큼 떨어진) 원소끼리 swap하기 때문에, 그 사이에 있는 같은 값의 상대적 순서가 바뀔 수 있음 (선택 정렬과 같은 이유) |

## 6. 개념 ↔ 코드 대응표

| 개념 | 코드 위치 |
|---|---|
| 간격 수열 초기값 | `gap = size // 2` (`sorting.py:48`) |
| 간격이 0이 될 때까지 반복 | `while gap > 0` (`sorting.py:49`) |
| gap만큼 떨어진 원소를 삽입 정렬 방식으로 비교 | `for j in range(i, gap - 1, -gap)` (`sorting.py:51`) |
| gap만큼 떨어진 두 원소 swap | `array[j - gap], array[j] = array[j], array[j - gap]` (`sorting.py:56`) |
| 다음 패스를 위해 간격을 절반으로 축소 | `gap //= 2` (`sorting.py:58`) |

## 7. 직접 실행해보기

```bash
python3 -m algorithm.sort.sorting
```

출력의 `shell sort` 줄을 확인하세요. `tests/sort/test_sorting.py`의 `IN_PLACE_ALGORITHMS` 딕셔너리(`tests/sort/test_sorting.py:11`)에 `shell_sort`가 등록되어 있어 다른 비교 기반 알고리즘들과 동일한 랜덤/엣지 케이스 테스트를 함께 통과하는지 확인할 수 있습니다.

---

[← 이전 문서: INSERTION_SORT.md](./INSERTION_SORT.md) | [목차: README.md](./README.md) | 다음 문서: [MERGE_SORT.md →](./MERGE_SORT.md)
