# 버킷 정렬 (Bucket Sort)

> 구현: [`sorting.py`](./sorting.py) — `Sort.bucket_sort()` (`sorting.py:224`)
> 이전 문서: [RADIX_SORT.md](./RADIX_SORT.md) · 목차: [README.md](./README.md)

## 1. 왜 이 알고리즘이 필요한가?

카운팅 정렬과 라딕스 정렬은 정수처럼 "이산적인(discrete)" 값에 특화되어 있습니다. 하지만 데이터가 `0.0 ~ 1.0` 사이의 실수처럼 **연속적인 값**이거나, 정수라도 값의 범위가 원소 개수보다 훨씬 커서 카운팅 정렬을 그대로 쓰기 부담스러운 경우가 있습니다.

버킷 정렬은 **"값의 범위를 여러 구간(bucket)으로 나누고, 각 원소를 자기 값에 해당하는 구간에 던져 넣은 뒤, 각 구간을 작게 나눠서 정렬한다"** 는 아이디어로 이 문제를 다룹니다. 데이터가 값의 범위에 고르게 분포되어 있을수록 각 버킷에 들어가는 원소 수가 적어지고, 작은 버킷은 정렬 비용이 거의 들지 않으므로 전체적으로 `O(n)`에 가까운 성능을 낼 수 있습니다.

## 2. 핵심 아이디어: 분배(distribute) → 버킷별 정렬 → 이어붙이기(concatenate)

`[29, 25, 3, 49, 9, 37, 21, 43]` (원소 8개, 기본 `bucket_count = len(array) = 8`)를 정렬해봅시다. `min_val=3`, `max_val=49`.

### 2-1. 값의 상대적 위치로 버킷 인덱스 계산 (분배)

```
index = int((value - min_val) / (max_val - min_val) * bucket_count)

  29 → int((26/46) * 8) = int(4.52) = 4
  25 → int((22/46) * 8) = int(3.83) = 3
   3 → int(( 0/46) * 8) = int(0.00) = 0
  49 → int((46/46) * 8) = int(8.00) = 8 → bucket_count와 같으므로 마지막 버킷(7)으로 보정
   9 → int(( 6/46) * 8) = int(1.04) = 1
  37 → int((34/46) * 8) = int(5.91) = 5
  21 → int((18/46) * 8) = int(3.13) = 3
  43 → int((40/46) * 8) = int(6.96) = 6

버킷:  [0]:[3]  [1]:[9]  [2]:[]  [3]:[25, 21]  [4]:[29]  [5]:[37]  [6]:[43]  [7]:[49]
```

값이 클수록 뒤쪽 버킷에, 작을수록 앞쪽 버킷에 들어간다는 점에서 값의 "상대적 위치"만으로 배치가 정해집니다. 버킷 `3`처럼 **두 원소(`25`, `21`)가 같은 버킷에 몰리는 경우**도 생깁니다 — 이때는 버킷 안에서 다시 정렬이 필요합니다.

### 2-2. 버킷별로 정렬

```
버킷 3 = [25, 21] → insertion_sort 적용 → [21, 25]
(나머지 버킷은 원소가 0~1개라 이미 정렬된 상태)
```

### 2-3. 버킷 순서대로 이어붙이기

```
[3] + [9] + [] + [21, 25] + [29] + [37] + [43] + [49]
= [3, 9, 21, 25, 29, 37, 43, 49]   ✅ 정렬 완료
```

## 3. "버킷 정렬은 비교하지 않는 정렬"이라는 통념 vs 이 구현체

카운팅/라딕스 정렬과 함께 묶여서 "버킷 정렬은 비교 기반이 아니다"라고 설명되는 경우가 많습니다. 이 말은 **절반만 맞습니다.**

- **분배(distribute) 단계**는 맞습니다 — `index = int((value - min_val) / (max_val - min_val) * bucket_count)`(`sorting.py:245`)는 원소끼리 서로 비교하지 않고, 각 값의 위치를 산술 연산만으로 계산합니다.
- 하지만 **버킷 안에서 정렬하는 단계**는 다릅니다. 위 예시의 버킷 `3`처럼 한 버킷에 원소가 여러 개 몰리면 그 안에서 다시 정렬해야 하는데, 이 구현체는 [INSERTION_SORT.md](./INSERTION_SORT.md)에서 다룬 **`insertion_sort`를 그대로 재사용**합니다(`sorting.py:257`). 삽입 정렬은 명백히 **비교 기반** 알고리즘입니다.

즉 이 구현체의 버킷 정렬은 "분배는 비교 없이, 버킷 내부 정렬은 비교 기반으로" 동작하는 **혼합형**입니다. `tests/sort/test_sorting.py:15-17`의 주석도 이 점을 명시적으로 짚고 있습니다.

```python
# bucket_sort distributes by value magnitude, but sorts each bucket with
# insertion_sort, so it is comparison-based just like the others here.
"bucket_sort": Sort.bucket_sort,
```

그래서 이 저장소의 테스트에서도 `bucket_sort`는 카운팅/라딕스 정렬이 속한 `NON_COMPARISON_ALGORITHMS`가 아니라, 버블/선택/삽입/퀵/병합/힙 정렬과 같은 `IN_PLACE_ALGORITHMS`(비교 기반) 그룹에 속해 있습니다(`tests/sort/test_sorting.py:7-18`). 실제로 `bucket_sort`는 다른 비교 기반 정렬들과 똑같이 `comp` 파라미터를 받아 오름차순/내림차순을 자유롭게 바꿀 수 있습니다 — 이 부분은 값을 셀 뿐 비교하지 않는 카운팅/라딕스 정렬은 흉내 낼 수 없는 유연성입니다.

## 4. `comp`가 버킷을 훑는 "방향"까지 결정한다

버킷 자체는 항상 **값이 작은 순서대로** 왼쪽(`index 0`)부터 큰 순서대로 오른쪽(`index bucket_count-1`)까지 채워집니다(2-1절). 그런데 `comp`로 내림차순을 요청했다면, 버킷을 채우는 순서는 그대로 둔 채 **버킷을 훑는 방향만 뒤집어서** 큰 값이 담긴 버킷부터 이어붙여야 합니다.

```python
bucket_indices = range(bucket_count) if not comp(min_val, max_val) else range(bucket_count - 1, -1, -1)
```

(`sorting.py:252`)

| `comp` | `comp(min_val, max_val)` | `bucket_indices` 방향 | 결과 |
|---|---|---|---|
| 기본값 `lambda a, b: a > b` (오름차순) | `min_val > max_val` → 항상 `False` | 정방향 `0 → bucket_count-1` | 오름차순 |
| `lambda a, b: a < b` (내림차순) | `min_val < max_val` → 항상 `True` | 역방향 `bucket_count-1 → 0` | 내림차순 |

`min_val == max_val`인 경우는 이미 앞에서(`sorting.py:232-233`) 조기 반환되므로, `comp(min_val, max_val)`는 항상 명확하게 참/거짓 중 하나로 결정됩니다. 이렇게 "버킷을 채우는 방향(항상 오름차순)"과 "버킷을 읽는 방향(comp에 따라 가변)"을 분리한 덕분에, 분배 로직을 건드리지 않고도 정렬 방향을 뒤집을 수 있습니다.

## 5. 코드 살펴보기

```python
@classmethod
def bucket_sort(cls, array, comp=lambda a, b: a > b, bucket_count=None):
    if len(array) <= 1:
        return array

    min_val = min(array)
    max_val = max(array)

    if min_val == max_val:
        return array

    if bucket_count is None:
        bucket_count = len(array)

    if bucket_count < 1:
        raise ValueError("bucket_count must be at least 1.")

    buckets = [[] for _ in range(bucket_count)]

    for value in array:
        index = int((value - min_val) / (max_val - min_val) * bucket_count)
        if index == bucket_count:
            index -= 1
        buckets[index].append(value)

    bucket_indices = range(bucket_count) if not comp(min_val, max_val) else range(bucket_count - 1, -1, -1)

    sorted_array = []
    for index in bucket_indices:
        cls.insertion_sort(buckets[index], comp)
        sorted_array.extend(buckets[index])

    array[:] = sorted_array
    return array
```

- **모든 값이 같은 경우 조기 반환**(`sorting.py:232-233`): `min_val == max_val`이면 이미 정렬된 것이나 다름없으므로 즉시 반환. 이 검사가 없으면 다음 줄의 `index = int((value - min_val) / (max_val - min_val) * ...)`에서 `max_val - min_val = 0`이 되어 0으로 나누는 오류(`ZeroDivisionError`)가 발생합니다.
- `bucket_count`(`sorting.py:235-236`): 지정하지 않으면 원소 개수만큼 버킷을 만듭니다(원소당 평균 1개씩 들어가도록 하는 경험적 기본값).
- `bucket_count`가 `1`보다 작으면 `ValueError`(`sorting.py:238-239`).
- **경계값 보정**(`sorting.py:246-247`): `value == max_val`인 원소는 계산식이 정확히 `bucket_count`가 되어 범위를 벗어나므로, 마지막 버킷(`bucket_count - 1`)으로 강제 보정합니다.
- 버킷별 정렬은 `cls.insertion_sort(buckets[index], comp)`(`sorting.py:257`)로 — 같은 `comp`를 그대로 전달해 버킷 내부 정렬 방향과 버킷 간 정렬 방향이 항상 일치하도록 합니다.

## 6. 시간복잡도 / 공간복잡도 / 안정성

| 항목 | 값 | 설명 |
|---|---|---|
| 최선(Best) | `O(n + k)` | 원소가 버킷에 고르게(1개씩) 분산되는 경우. `k`=버킷 개수 |
| 평균(Average) | `O(n + k)` | 데이터가 값의 범위에 고르게 분포되어 있다고 가정할 때 |
| 최악(Worst) | `O(n²)` | 모든 원소가 하나의 버킷에 몰리면, 그 버킷 하나에 대해 삽입 정렬(`O(n²)`)을 수행하는 것과 같아짐 |
| 공간(Space) | `O(n + k)` | 버킷 리스트 `k`개 + 결과 배열 `n`개 |
| 안정성(Stable) | ✅ 안정 | 같은 값은 항상 같은 버킷으로 분배되고(`index` 계산이 결정적), 버킷 내부 정렬(`insertion_sort`)도 안정적이므로 전체적으로 안정 정렬 |

## 7. 개념 ↔ 코드 대응표

| 개념 | 코드 위치 |
|---|---|
| 0으로 나누기 방지(모든 값이 동일한 경우) | `if min_val == max_val: return array` (`sorting.py:232-233`) |
| 값의 상대적 위치로 버킷 인덱스 계산(비교 없는 분배) | `index = int((value - min_val) / (max_val - min_val) * bucket_count)` (`sorting.py:245`) |
| 최댓값의 경계 보정 | `if index == bucket_count: index -= 1` (`sorting.py:246-247`) |
| comp에 따라 버킷을 읽는 방향 결정 | `bucket_indices = range(...) if not comp(...) else range(...)` (`sorting.py:252`) |
| 버킷 내부 정렬(비교 기반, 삽입 정렬 재사용) | `cls.insertion_sort(buckets[index], comp)` (`sorting.py:257`) |

## 8. 직접 실행해보기

```bash
python3 -m algorithm.sort.sorting
```

출력의 `bucket sort` 줄을 확인하세요. `bucket_sort`가 다른 비교 기반 정렬들과 동일한 엣지 케이스(빈 배열, 단일 원소, 중복값, 커스텀 comparator)를 통과하는지는 `tests/sort/test_sorting.py`의 `IN_PLACE_ALGORITHMS` 파라미터화 테스트(`tests/sort/test_sorting.py:7-18`)에서 확인할 수 있습니다.

---

[← 이전 문서: RADIX_SORT.md](./RADIX_SORT.md) | [목차: README.md](./README.md)

(이 문서는 목차의 마지막 문서이므로 다음 문서가 없습니다.)
