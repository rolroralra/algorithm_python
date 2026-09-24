# 병합 정렬 (Merge Sort)

> 구현: [`sorting.py`](./sorting.py) — `Sort.merge_sort()` (`sorting.py:61`)
> 이전 문서: [SHELL_SORT.md](./SHELL_SORT.md) · 목차: [README.md](./README.md)

## 1. 왜 이 알고리즘이 필요한가?

지금까지 본 버블/선택/삽입/쉘 정렬은 모두 **최악의 경우 `O(n²)`** 입니다. 데이터가 조금만 커져도 급격히 느려집니다.

병합 정렬은 **"분할 정복(Divide and Conquer)"** 전략으로 이 문제를 해결합니다. "큰 배열을 정렬하기 어렵다면, 반으로 쪼개서 각각 정렬한 뒤 합치자"는 아이디어입니다. 절반씩 쪼개는 과정을 재귀적으로 반복하면 결국 원소 1개짜리 배열(항상 정렬된 상태)까지 내려가고, 그 다음부터는 "이미 정렬된 두 배열을 합치는 것"만 반복하면 됩니다. 이 전략 덕분에 **항상** `O(n log n)`을 보장합니다 — 최선/평균/최악이 모두 동일합니다.

## 2. 핵심 아이디어: 분할(divide) → 정복(정렬) → 병합(merge)

```
                     [5, 3, 8, 1]
                    /            \
              [5, 3]              [8, 1]
              /    \              /    \
            [5]    [3]          [8]    [1]     ← 원소 1개, 항상 정렬됨(재귀 종료)
              \    /              \    /
              [3, 5]              [1, 8]        ← 두 정렬된 배열을 병합(merge)
                    \            /
                    [1, 3, 5, 8]                 ← 최종 병합 결과
```

재귀로 계속 반으로 쪼개는 부분(divide)은 사실 아무 일도 하지 않습니다. 진짜 "정렬"은 쪼개고 올라오면서 **두 정렬된 배열을 합치는 병합(merge) 단계**에서 일어납니다.

### 병합(merge)이 하는 일

이미 정렬된 두 배열 `[3, 5]`와 `[1, 8]`을 합쳐 `[1, 3, 5, 8]`을 만드는 과정:

```
[3, 5]          [1, 8]
  ↑               ↑
 i=0             j=0     비교: 3 vs 1 → 1이 더 작음 → 결과에 1 추가, j += 1
                   ↑
                  j=1     비교: 3 vs 8 → 3이 더 작음 → 결과에 3 추가, i += 1
  ↑
 i=1                      비교: 5 vs 8 → 5가 더 작음 → 결과에 5 추가, i += 1
                          왼쪽 배열 소진 → 오른쪽 남은 원소(8)를 그대로 복사

결과: [1, 3, 5, 8]
```

양쪽 배열의 맨 앞 원소끼리만 비교하면 되는 이유는, **두 배열이 각각 이미 정렬되어 있기 때문**입니다.

## 3. 코드 살펴보기

### 3-1. 분할 (`merge_sort` / `__merge_sort`)

```python
@classmethod
def merge_sort(cls, array, comp=lambda a, b: a > b):
    cls.__merge_sort(array, 0, len(array), comp)

@classmethod
def __merge_sort(cls, array, start_inclusive, end_exclusive, comp=lambda a, b: a > b):
    if end_exclusive - start_inclusive <= 1:
        return

    mid = (start_inclusive + end_exclusive) // 2
    cls.__merge_sort(array, start_inclusive, mid, comp)
    cls.__merge_sort(array, mid, end_exclusive, comp)
    cls.__merge(array, start_inclusive, mid, end_exclusive, comp)
```

- `merge_sort()`(`sorting.py:61-62`)는 공개 진입점으로, 내부적으로 `[0, len(array))` 전체 범위에 대해 private 헬퍼 `__merge_sort()`를 호출합니다.
- **재귀 종료 조건**(`sorting.py:66-67`): 구간 길이가 `1` 이하이면(원소가 0개 또는 1개) 이미 정렬된 것이므로 그냥 반환.
- **분할**(`sorting.py:70`): 중간 지점 `mid`를 기준으로 왼쪽 절반 `[start, mid)`과 오른쪽 절반 `[mid, end)`을 각각 재귀 호출(`sorting.py:71-72`)로 정렬.
- **병합**(`sorting.py:74`): 두 절반이 각각 정렬 완료된 후, `__merge()`로 하나로 합칩니다.

### 3-2. 병합 (`__merge`)

```python
@classmethod
def __merge(cls, array, start_inclusive, mid, end_exclusive, comp=lambda a, b: a > b):
    i = start_inclusive
    j = mid
    k = 0

    merged_array = [0] * (end_exclusive - start_inclusive)

    while i < mid and j < end_exclusive:
        if comp(array[i], array[j]):
            merged_array[k] = array[j]
            j += 1
        else:
            merged_array[k] = array[i]
            i += 1
        k += 1

    while i < mid:
        merged_array[k] = array[i]
        i += 1
        k += 1

    while j < end_exclusive:
        merged_array[k] = array[j]
        j += 1
        k += 1

    array[start_inclusive:end_exclusive] = merged_array[0:k]
```

- `i`는 왼쪽 절반을 가리키는 포인터, `j`는 오른쪽 절반을 가리키는 포인터, `k`는 결과 배열 `merged_array`에 채워 넣을 위치(`sorting.py:78-80`).
- **핵심 병합 루프**(`sorting.py:85-92`): 양쪽 포인터가 모두 자기 구간 안에 있는 동안, `comp(array[i], array[j])`로 어느 쪽을 먼저 가져올지 비교합니다. `comp(array[i], array[j])`가 `True`(왼쪽이 뒤에 와야 함)이면 오른쪽 값을 먼저 채우고, 아니면 왼쪽 값을 채웁니다.
  - **중요**: 두 값이 "같다고" 판단될 때(`comp`가 `False`)는 `else` 분기로 가서 **왼쪽(`array[i]`)을 먼저** 채웁니다. 왼쪽 절반이 원래 배열에서 더 앞쪽 구간이었으므로, 이 규칙이 바로 병합 정렬을 **안정 정렬**로 만드는 핵심입니다.
- **잔여 원소 복사**(`sorting.py:95-104`): 한쪽 구간이 먼저 소진되면, 남은 쪽은 이미 정렬되어 있으므로 비교 없이 그대로 복사만 하면 됩니다.
- **원본에 반영**(`sorting.py:106`): 임시 배열 `merged_array`의 내용을 슬라이스 대입으로 원본 `array[start_inclusive:end_exclusive]`에 덮어씁니다.

## 4. 시간복잡도 / 공간복잡도 / 안정성

| 항목 | 값 | 설명 |
|---|---|---|
| 최선(Best) | `O(n log n)` | 분할 정복 구조상 데이터 상태와 무관하게 항상 동일 |
| 평균(Average) | `O(n log n)` | |
| 최악(Worst) | `O(n log n)` | 병합 정렬의 가장 큰 장점: **최악의 경우도 `O(n log n)`을 보장** |
| 공간(Space) | `O(n)` | 병합할 때마다 임시 배열 `merged_array`(`sorting.py:82`)를 새로 만듦 (in-place가 아님) |
| 안정성(Stable) | ✅ 안정 | 값이 같을 때 항상 왼쪽 절반의 원소를 먼저 채우는 `else` 분기(`sorting.py:89-91`) 덕분 |

재귀 깊이는 `log₂n`이고, 각 깊이에서 전체 원소 `n`개를 한 번씩 병합하므로 `n × log n`, 즉 `O(n log n)`이 나옵니다. 이 비용이 데이터의 초기 배치와 무관하다는 점이 다른 `O(n²)` 알고리즘들과의 결정적 차이입니다.

## 5. 개념 ↔ 코드 대응표

| 개념 | 코드 위치 |
|---|---|
| 분할 정복의 진입점 | `merge_sort()` → `__merge_sort()` (`sorting.py:61`, `65`) |
| 재귀 종료 조건(원소 0~1개) | `if end_exclusive - start_inclusive <= 1: return` (`sorting.py:66-67`) |
| 왼쪽/오른쪽 절반으로 분할 | `mid = (start_inclusive + end_exclusive) // 2` (`sorting.py:70`) |
| 두 정렬된 절반을 합치는 병합 | `__merge()` (`sorting.py:77`) |
| 안정성을 보장하는 "동점이면 왼쪽 우선" 규칙 | `else: merged_array[k] = array[i]` (`sorting.py:89-91`) |
| 임시 배열을 원본에 반영 | `array[start_inclusive:end_exclusive] = merged_array[0:k]` (`sorting.py:106`) |

## 6. 직접 실행해보기

```bash
python3 -m algorithm.sort.sorting
```

출력의 `merge sort` 줄을 확인하세요. `Sort.sort()`가 원본 배열을 변경하지 않는지 확인하는 테스트인 `test_does_not_mutate_input_array`(`tests/sort/test_sorting.py:117-122`)가 바로 `merge_sort`를 사용해 이 성질을 검증합니다.

---

[← 이전 문서: SHELL_SORT.md](./SHELL_SORT.md) | [목차: README.md](./README.md) | 다음 문서: [QUICK_SORT.md →](./QUICK_SORT.md)
