# 버블 정렬 (Bubble Sort)

> 구현: [`sorting.py`](./sorting.py) — `Sort.bubble_sort()` (`sorting.py:21`)
> 목차로 돌아가기: [README.md](./README.md)

## 1. 왜 이 알고리즘부터 배우는가?

버블 정렬은 정렬 알고리즘 중 가장 직관적입니다. **"이웃한 두 원소를 비교해서, 순서가 뒤바뀌어 있으면 그 자리에서 바로 swap한다"** 는 규칙 하나만 계속 반복합니다.

이름이 "버블(bubble, 거품)"인 이유는, 한 번의 순회(pass)가 끝날 때마다 그 구간에서 가장 큰(혹은 comparator 기준으로 "가장 뒤에 있어야 할") 값이 마치 물속 거품처럼 배열의 맨 끝으로 떠오르기 때문입니다.

## 2. 핵심 동작: 이웃 교환(swap)이 오른쪽 끝으로 값을 밀어냄

`[5, 3, 8, 1]`을 오름차순으로 정렬하는 첫 번째 pass를 봅시다.

```
초기: [5, 3, 8, 1]

j=0: 5 > 3 → swap        [3, 5, 8, 1]
j=1: 5 > 8 ? No           [3, 5, 8, 1]
j=2: 8 > 1 → swap        [3, 5, 1, 8]
                                    ↑
                         가장 큰 값 8이 맨 끝으로 이동 (확정)
```

한 번의 pass가 끝나면 배열의 **가장 오른쪽 원소는 이미 최종 위치가 확정**됩니다. 그래서 다음 pass는 마지막 원소를 제외하고 한 칸씩 범위를 줄여나갑니다.

```
pass 1 대상 범위: index 0 ~ 3  → 최댓값이 index 3에 확정
pass 2 대상 범위: index 0 ~ 2  → 그 다음 최댓값이 index 2에 확정
pass 3 대상 범위: index 0 ~ 1  → 이제 남은 두 원소만 비교
```

## 3. 코드 살펴보기

```python
@staticmethod
def bubble_sort(array, comp=lambda a, b: a > b):
    size = len(array)
    for i in range(size - 1):
        is_swapped = False
        for j in range(size - i - 1):
            if comp(array[j], array[j + 1]):
                is_swapped = True
                array[j], array[j + 1] = array[j + 1], array[j]

        if not is_swapped:
            break
```

- 바깥쪽 `for i in range(size - 1)`(`sorting.py:23`): 총 pass 횟수. `size - i - 1`(`sorting.py:25`)로 안쪽 루프 범위를 매 pass마다 1씩 줄여서, 이미 확정된 오른쪽 구간은 다시 비교하지 않습니다.
- 안쪽 `for j in ...`(`sorting.py:25`): 이웃한 `array[j]`와 `array[j+1]`을 비교(`sorting.py:26`)하고, `comp(array[j], array[j+1])`가 `True`이면(즉 순서가 뒤바뀌어 있으면) swap(`sorting.py:28`).
- **조기 종료(early-exit) 최적화**: `is_swapped` 플래그(`sorting.py:24`, `sorting.py:27`)로 이번 pass에서 단 한 번도 swap이 일어나지 않았다면, 이미 배열이 정렬 완료된 상태라는 뜻이므로 `break`(`sorting.py:31-32`)로 즉시 종료합니다. 이 최적화 덕분에 **이미 정렬된 배열**에서는 단 한 번의 pass(`O(n)`)만에 끝납니다.

## 4. 시간복잡도 / 공간복잡도 / 안정성

| 항목 | 값 | 설명 |
|---|---|---|
| 최선(Best) | `O(n)` | 이미 정렬된 배열 → 첫 pass에서 swap 0번 → early-exit |
| 평균(Average) | `O(n²)` | 무작위 데이터 |
| 최악(Worst) | `O(n²)` | 완전히 역순으로 정렬된 배열 |
| 공간(Space) | `O(1)` | 추가 배열 없이 원본 배열 안에서 swap만 수행(in-place) |
| 안정성(Stable) | ✅ 안정 | `comp(array[j], array[j+1])`가 `True`일 때만 swap하므로, 두 값이 "같다"고 판단되면(즉 `comp`가 `False`) 절대 순서를 바꾸지 않습니다 → 같은 값의 상대적 순서가 유지됩니다 |

## 5. 개념 ↔ 코드 대응표

| 개념 | 코드 위치 |
|---|---|
| 이웃 원소 비교 | `comp(array[j], array[j + 1])` (`sorting.py:26`) |
| swap(교환) | `array[j], array[j + 1] = array[j + 1], array[j]` (`sorting.py:28`) |
| pass마다 비교 범위 축소 | `range(size - i - 1)` (`sorting.py:25`) |
| 조기 종료 최적화 | `is_swapped` 플래그, `if not is_swapped: break` (`sorting.py:24`, `27`, `31-32`) |

## 6. 직접 실행해보기

```bash
python3 -m algorithm.sort.sorting
```

출력에서 `bubble sort` 로 시작하는 줄을 확인하세요. 커스텀 comparator로 내림차순 정렬을 테스트하는 예시는 `tests/sort/test_sorting.py:35-38`(`test_sorts_descending_with_custom_comparator`)에서 확인할 수 있습니다.

---

[← README.md로 돌아가기](./README.md) | 다음 문서: [SELECTION_SORT.md →](./SELECTION_SORT.md)

(이 문서는 목차의 첫 번째 문서이므로 이전 문서가 없습니다.)
