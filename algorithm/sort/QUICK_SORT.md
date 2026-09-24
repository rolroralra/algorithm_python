# 퀵 정렬 (Quick Sort)

> 구현: [`sorting.py`](./sorting.py) — `Sort.quick_sort()` (`sorting.py:109`)
> 이전 문서: [MERGE_SORT.md](./MERGE_SORT.md) · 목차: [README.md](./README.md)

## 1. 왜 이 알고리즘이 필요한가?

병합 정렬은 항상 `O(n log n)`을 보장하지만, 병합 단계마다 **추가 배열을 새로 만들어야 해서(`O(n)` 공간)** 메모리를 많이 씁니다.

퀵 정렬도 병합 정렬처럼 분할 정복(Divide and Conquer)을 쓰지만, 방식이 다릅니다. 병합 정렬은 "먼저 반으로 쪼개고, 나중에 합치면서 정렬"하는 반면, 퀵 정렬은 **"먼저 기준값(pivot)보다 작은 값과 큰 값으로 미리 정렬해서 쪼개고, 합치는 과정이 아예 필요 없게"** 만듭니다. 이 덕분에 평균적으로 병합 정렬과 같은 `O(n log n)`이면서도, 추가 배열 없이 원본 배열 안에서 swap만으로 동작(in-place에 가까움)합니다. 실무에서 범용 정렬 알고리즘으로 가장 많이 쓰이는 이유입니다.

## 2. 핵심 아이디어: 피벗(pivot) 기준으로 분할(partition)

퀵 정렬의 한 단계(partition)는 배열에서 임의의 값 하나를 **피벗(pivot)** 으로 고른 뒤, "피벗보다 작은 값은 왼쪽, 큰 값은 오른쪽"으로 재배치하고 **피벗을 그 경계 자리에 확정**시키는 것입니다.

```
[5, 3, 8, 1, 9]   pivot으로 5를 선택(맨 앞으로 swap해서 고정)했다고 가정

  5는 왼쪽 끝에 고정, index(작은 값의 경계)는 pivot 위치에서 시작

  i=1: 3 < 5 → 작은 값 그룹으로 편입
  i=2: 8 ≥ 5 → 그대로 둠(오른쪽에 남김)
  i=3: 1 < 5 → 작은 값 그룹으로 편입 (8과 자리 교환)
  i=4: 9 ≥ 5 → 그대로 둠

  훑기 완료 후:      [5, 3, 1, 8, 9]
                         └작음┘  └큼┘
  마지막으로 pivot(5)을 경계 위치로 swap:

  최종:              [1, 3, 5, 8, 9]
                      └작음┘ ↑  └큼┘
                          pivot 최종 위치(index=2) 확정
```

피벗이 제자리를 찾고 나면, **왼쪽 구간(`[1, 3]`)과 오른쪽 구간(`[8, 9]`)은 서로 완전히 독립적**입니다. 이제 이 두 구간을 각각 재귀적으로 같은 방식으로 정렬하면 전체가 정렬됩니다. 병합 정렬과 달리 "합치는" 단계가 필요 없다는 점이 핵심입니다.

## 3. 코드 살펴보기

### 3-1. 재귀 골격 (`quick_sort` / `__quick_sort`)

```python
@classmethod
def quick_sort(cls, array, comp=lambda a, b: a > b):
    cls.__quick_sort(array, 0, len(array), comp)

@classmethod
def __quick_sort(cls, array, start_inclusive, end_exclusive, comp=lambda a, b: a > b):
    if end_exclusive - start_inclusive <= 1:
        return

    final_pivot_index = cls.__partition_by_pivot_index(array, start_inclusive, end_exclusive, comp)
    cls.__quick_sort(array, start_inclusive, final_pivot_index, comp)
    cls.__quick_sort(array, final_pivot_index + 1, end_exclusive, comp)
```

- 재귀 종료 조건(`sorting.py:114-115`)은 병합 정렬과 동일하게 "원소 0~1개면 이미 정렬됨".
- `__partition_by_pivot_index()`(`sorting.py:118`)를 호출해 피벗을 제자리에 놓고, 그 최종 위치 `final_pivot_index`를 받습니다.
- 피벗을 제외한 **왼쪽 구간**(`sorting.py:120`)과 **오른쪽 구간**(`sorting.py:121`)을 각각 재귀 정렬합니다. 병합 정렬과 달리 이후 합치는 단계가 없습니다.

### 3-2. 분할(partition) 로직

```python
@classmethod
def __partition_by_pivot_index(cls, array, start_inclusive, end_exclusive, comp=lambda a, b: a > b):
    pivot_index = start_inclusive + secrets.randbelow(end_exclusive - start_inclusive)
    pivot = array[pivot_index]

    array[pivot_index], array[start_inclusive] = array[start_inclusive], array[pivot_index]

    index = start_inclusive
    for i in range(start_inclusive + 1, end_exclusive):
        if comp(pivot, array[i]):
            index += 1
            array[index], array[i] = array[i], array[index]

    array[start_inclusive], array[index] = array[index], array[start_inclusive]

    return index
```

- **무작위 피벗 선택**(`sorting.py:126`): `secrets.randbelow()`로 구간 내에서 피벗 인덱스를 무작위로 고릅니다. `random` 모듈 대신 암호학적으로 안전한 `secrets`를 사용해, 입력 데이터를 미리 알고 있는 경우에도 피벗 선택 패턴을 예측하기 어렵게 만들어 `O(n²)` 최악의 경우를 유발하는 적대적 입력을 방지합니다.
- 고른 피벗을 구간의 맨 앞(`start_inclusive`)으로 swap(`sorting.py:129`)해 계산을 단순화합니다(Lomuto partition 방식).
- `index`(`sorting.py:132`)는 "지금까지 피벗보다 작다고 확인된 값들"의 경계입니다. `start_inclusive`에서 시작합니다.
- 순회하며(`sorting.py:133`) `comp(pivot, array[i])`가 `True`이면(피벗이 `array[i]`보다 뒤에 와야 한다 = `array[i]`가 더 작다) 경계를 한 칸 넓히고(`index += 1`) 그 자리와 swap(`sorting.py:135-136`)해서 작은 값 그룹 안으로 편입시킵니다.
- 순회가 끝나면 맨 앞에 있던 피벗을 경계 위치(`index`)로 swap(`sorting.py:138`)해 최종 제자리에 확정시키고, 그 인덱스를 반환합니다.

## 4. 시간복잡도 / 공간복잡도 / 안정성

| 항목 | 값 | 설명 |
|---|---|---|
| 최선(Best) | `O(n log n)` | 매번 균형 잡힌 분할이 일어날 때 |
| 평균(Average) | `O(n log n)` | 무작위 피벗 덕분에 대부분의 입력에서 균형 잡힌 분할이 나옴 |
| 최악(Worst) | `O(n²)` | 매번 극단적으로 불균형한 분할이 일어날 때(예: 항상 최솟값/최댓값이 피벗으로 뽑힘). 무작위 피벗을 쓰더라도 이론상 발생 가능은 하지만 확률이 매우 낮음 |
| 공간(Space) | 평균 `O(log n)`, 최악 `O(n)` | 추가 배열은 없지만 재귀 호출 스택 깊이만큼 공간을 사용(in-place) |
| 안정성(Stable) | ❌ 불안정 | 분할 과정에서 **멀리 떨어진 원소끼리 swap**(`sorting.py:135-136`, `138`)하기 때문에 같은 값의 상대적 순서가 바뀔 수 있음 |

병합 정렬과의 핵심 차이는 "최악의 경우 보장" 여부입니다. 병합 정렬은 항상 `O(n log n)`을 보장하는 대신 `O(n)` 공간이 필요하고, 퀵 정렬은 평균은 더 빠르고 공간도 적게 쓰지만 최악의 경우 `O(n²)`로 느려질 위험을 감수합니다.

## 5. 개념 ↔ 코드 대응표

| 개념 | 코드 위치 |
|---|---|
| 재귀 진입점 | `quick_sort()` → `__quick_sort()` (`sorting.py:109`, `112`) |
| 재귀 종료 조건 | `if end_exclusive - start_inclusive <= 1: return` (`sorting.py:114-115`) |
| 분할(partition) 후 좌/우 재귀 | `sorting.py:120-121` |
| 무작위 피벗 선택 | `secrets.randbelow(...)` (`sorting.py:126`) |
| 작은 값 그룹 경계 | 변수 `index` (`sorting.py:132`) |
| 작은 값을 경계 안으로 편입 | `if comp(pivot, array[i]): index += 1; swap` (`sorting.py:134-136`) |
| 피벗을 최종 위치로 확정 | `array[start_inclusive], array[index] = array[index], array[start_inclusive]` (`sorting.py:138`) |

## 6. 직접 실행해보기

```bash
python3 -m algorithm.sort.sorting
```

`Sort.sort()`의 기본 알고리즘이 바로 `quick_sort`입니다(`sorting.py:264-265`). 출력의 `quick sort` 줄과 함께, `test_default_algorithm_is_ascending_quick_sort`(`tests/sort/test_sorting.py:114-115`)에서 이 기본값을 검증하는 테스트를 확인할 수 있습니다.

---

[← 이전 문서: MERGE_SORT.md](./MERGE_SORT.md) | [목차: README.md](./README.md) | 다음 문서: [HEAP_SORT.md →](./HEAP_SORT.md)
