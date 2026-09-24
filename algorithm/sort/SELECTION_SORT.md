# 선택 정렬 (Selection Sort)

> 구현: [`sorting.py`](./sorting.py) — `Sort.selection_sort()` (`sorting.py:8`)
> 이전 문서: [BUBBLE_SORT.md](./BUBBLE_SORT.md) · 목차: [README.md](./README.md)

## 1. 왜 이 알고리즘이 필요한가?

버블 정렬은 매번 "이웃끼리" swap하느라 swap 횟수가 많습니다. 선택 정렬은 발상을 바꿔서, **"남은 구간에서 정렬 기준상 가장 먼저 와야 할 값을 딱 한 번만 찾아서, 그 값을 현재 위치와 통째로 swap한다"** 는 전략을 씁니다.

결과적으로 선택 정렬은 한 pass당 swap이 **최대 1번**만 일어납니다. swap(쓰기 연산) 비용이 비교보다 훨씬 비싼 환경(예: 메모리 쓰기가 느린 하드웨어)에서 유리한 이유입니다. 다만 "가장 먼저 와야 할 값"을 찾기 위한 비교 횟수 자체는 버블 정렬과 동일하게 `O(n²)`입니다.

## 2. 핵심 동작: 매 라운드마다 "정답 후보"를 하나씩 확정

`[5, 3, 8, 1]`을 오름차순으로 정렬하는 과정입니다.

```
초기:        [5, 3, 8, 1]
              ↑ i=0부터 탐색 시작

i=0 라운드: 남은 구간 [5, 3, 8, 1] 중 최솟값 탐색 → 1 (index 3)
            array[0]과 array[3] swap
          → [1, 3, 8, 5]
             확정 ↑

i=1 라운드: 남은 구간 [3, 8, 5] 중 최솟값 탐색 → 3 (index 1, 이미 제자리)
            array[1]과 array[1] swap(제자리이므로 사실상 변화 없음)
          → [1, 3, 8, 5]
                확정 ↑

i=2 라운드: 남은 구간 [8, 5] 중 최솟값 탐색 → 5 (index 3)
            array[2]와 array[3] swap
          → [1, 3, 5, 8]
                   확정 ↑
```

매 라운드가 끝날 때마다 **왼쪽부터 하나씩 최종 위치가 확정**된다는 점은 버블 정렬과 비슷하지만, 버블 정렬은 "매 비교마다" swap이 일어날 수 있는 반면 선택 정렬은 "라운드당 최대 1번"만 swap이 일어난다는 차이가 있습니다.

## 3. 코드 살펴보기

```python
@staticmethod
def selection_sort(array, comp=lambda a, b: a > b):
    size = len(array)
    for i in range(size):
        selected_index = i
        selected_element = array[i]
        for j in range(i + 1, size):
            if comp(selected_element, array[j]):
                selected_index = j
                selected_element = array[j]

        array[i], array[selected_index] = array[selected_index], array[i]
```

- 바깥쪽 `for i in range(size)`(`sorting.py:10`): 이번 라운드에 "확정시킬" 위치.
- `selected_index`, `selected_element`(`sorting.py:11-12`): 지금까지 찾은 "정답 후보"(기본 comparator 기준 최솟값)의 인덱스와 값. 처음엔 현재 위치 `i` 자신을 후보로 시작합니다.
- 안쪽 `for j in range(i + 1, size)`(`sorting.py:13`): 남은 구간을 훑으면서 `comp(selected_element, array[j])`가 `True`이면(즉 지금 후보가 `array[j]`보다 뒤에 와야 한다면) 후보를 `array[j]`로 교체(`sorting.py:14-16`).
- 라운드가 끝나면 `array[i]`와 최종 후보 `array[selected_index]`를 **딱 한 번** swap(`sorting.py:18`)합니다.

## 4. 시간복잡도 / 공간복잡도 / 안정성

| 항목 | 값 | 설명 |
|---|---|---|
| 최선(Best) | `O(n²)` | 이미 정렬되어 있어도 "최솟값 탐색"은 항상 남은 구간 전체를 훑어야 함 → 조기 종료 불가능 |
| 평균(Average) | `O(n²)` | |
| 최악(Worst) | `O(n²)` | |
| 공간(Space) | `O(1)` | 인덱스/값 몇 개만 추가로 사용(in-place) |
| 안정성(Stable) | ❌ 불안정 | 라운드마다 **멀리 떨어진 두 원소를 통째로 swap**하기 때문에, 같은 값이더라도 그 사이에 있던 다른 원소들과의 상대적 순서가 바뀔 수 있습니다. 예: `[3a, 3b, 1]`에서 `1`과 `3a`를 swap하면 `[1, 3b, 3a]`가 되어 `3a`, `3b`의 순서가 뒤집힘 |

버블 정렬과 선택 정렬 모두 비교 횟수는 `O(n²)`으로 같지만, **swap 횟수**와 **안정성**에서 차이가 난다는 점이 두 알고리즘을 비교할 때 핵심 포인트입니다.

## 5. 개념 ↔ 코드 대응표

| 개념 | 코드 위치 |
|---|---|
| 이번 라운드의 "정답 후보" 초기화 | `selected_index = i`, `selected_element = array[i]` (`sorting.py:11-12`) |
| 후보 갱신 조건 | `comp(selected_element, array[j])` (`sorting.py:14`) |
| 라운드당 단 한 번의 swap | `array[i], array[selected_index] = ...` (`sorting.py:18`) |

## 6. 직접 실행해보기

```bash
python3 -m algorithm.sort.sorting
```

출력의 `selection sort` 줄을 확인하세요. 안정성이 없다는 점은 `tests/sort/test_sorting.py`의 `test_array_with_duplicates`(중복값 케이스)를 직접 원소에 태그를 달아 실험해보면 체감할 수 있습니다.

---

[← 이전 문서: BUBBLE_SORT.md](./BUBBLE_SORT.md) | [목차: README.md](./README.md) | 다음 문서: [INSERTION_SORT.md →](./INSERTION_SORT.md)
