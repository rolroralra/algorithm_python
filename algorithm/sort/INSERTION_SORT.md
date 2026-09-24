# 삽입 정렬 (Insertion Sort)

> 구현: [`sorting.py`](./sorting.py) — `Sort.insertion_sort()` (`sorting.py:35`)
> 이전 문서: [SELECTION_SORT.md](./SELECTION_SORT.md) · 목차: [README.md](./README.md)

## 1. 왜 이 알고리즘이 필요한가?

카드 게임을 할 때 손에 든 카드를 정렬하는 방식을 떠올려보세요. 새 카드를 한 장 뽑으면, **이미 정렬되어 있는 손패 안의 알맞은 위치**에 그 카드를 끼워 넣습니다. 삽입 정렬이 정확히 이 방식으로 동작합니다.

배열을 "이미 정렬된 왼쪽 구간"과 "아직 정렬 안 된 오른쪽 구간"으로 나눠서 생각하면, 매 단계마다 오른쪽 구간의 맨 앞 원소를 하나 꺼내 왼쪽의 정렬된 구간 안 올바른 자리에 밀어 넣는 것입니다.

이 알고리즘은 **거의 정렬된 데이터**에 대해서 특히 빠릅니다 — 뒤에서 배울 쉘 정렬과 버킷 정렬의 각 버킷 내부 정렬(`sorting.py:257`)에서도 바로 이 특성 때문에 삽입 정렬이 재사용됩니다.

## 2. 핵심 동작: 정렬된 구간에 값을 한 칸씩 밀어 넣기

`[5, 3, 8, 1]`을 오름차순으로 정렬하는 과정입니다. `|`는 "정렬된 구간"과 "미정렬 구간"의 경계입니다.

```
초기:        5 | 3, 8, 1        (원소 1개는 항상 정렬된 상태로 간주)

i=1: 3을 꺼내서 왼쪽과 비교
     5 > 3 → 5를 오른쪽으로 한 칸 이동, 3을 그 자리에 삽입
     3, 5 | 8, 1

i=2: 8을 꺼내서 왼쪽과 비교
     5 > 8 ? No → 이미 제자리, 이동 없음
     3, 5, 8 | 1

i=3: 1을 꺼내서 왼쪽과 비교
     8 > 1 → 8 이동, 5 > 1 → 5 이동, 3 > 1 → 3 이동
     1, 3, 5, 8 |
```

`i=3` 라운드처럼 삽입할 값이 맨 앞까지 밀려 들어가야 하면 비교/swap이 `i`번 필요하지만, `i=2` 라운드처럼 **이미 제자리**라면 비교 단 1번으로 즉시 끝납니다. 이 "조기 종료"가 삽입 정렬이 거의 정렬된 데이터에서 빠른 이유입니다.

## 3. 코드 살펴보기

```python
@staticmethod
def insertion_sort(array, comp=lambda a, b: a > b):
    size = len(array)
    for i in range(1, size):
        for j in range(i, 0, -1):
            if not comp(array[j - 1], array[j]):
                break

            array[j - 1], array[j] = array[j], array[j - 1]
```

- 바깥쪽 `for i in range(1, size)`(`sorting.py:37`): `array[i]`를 "왼쪽의 정렬된 구간 `array[0..i-1]`"에 삽입할 차례입니다. `i=0`은 원소가 하나뿐이라 항상 정렬된 상태이므로 `range(1, size)`로 건너뜁니다.
- 안쪽 `for j in range(i, 0, -1)`(`sorting.py:38`): `j`를 `i`부터 `1`까지 **거꾸로** 내려가며, `array[j]`를 왼쪽 이웃 `array[j-1]`과 비교합니다.
- `if not comp(array[j-1], array[j]): break`(`sorting.py:40-41`): 왼쪽 이웃이 더 이상 순서를 어기지 않으면(=이미 제자리를 찾았으면) 즉시 break. 이 한 줄이 버블 정렬의 `is_swapped` 플래그와 같은 역할을 라운드 내부에서 수행합니다.
- `array[j - 1], array[j] = array[j], array[j - 1]`(`sorting.py:43`): 아직 순서가 어긋나 있으면 한 칸 swap하며 계속 왼쪽으로 이동.

## 4. 시간복잡도 / 공간복잡도 / 안정성

| 항목 | 값 | 설명 |
|---|---|---|
| 최선(Best) | `O(n)` | 이미 정렬된 배열이면 각 `i`마다 비교 1번 후 즉시 break |
| 평균(Average) | `O(n²)` | |
| 최악(Worst) | `O(n²)` | 완전 역순 배열 → 매번 맨 앞까지 밀어 넣어야 함 |
| 공간(Space) | `O(1)` | in-place, swap만 사용 |
| 안정성(Stable) | ✅ 안정 | `comp(array[j-1], array[j])`가 `True`일 때만(엄격히 순서가 어긋났을 때만) swap하므로 같은 값끼리는 절대 순서가 바뀌지 않음 |

## 5. 개념 ↔ 코드 대응표

| 개념 | 코드 위치 |
|---|---|
| 정렬된 구간 / 미정렬 구간 경계 | 바깥 루프 변수 `i` (`sorting.py:37`) |
| 왼쪽으로 밀어 넣기(오른쪽 이웃과 계속 비교/swap) | `for j in range(i, 0, -1)` (`sorting.py:38`) |
| 제자리를 찾으면 조기 종료 | `if not comp(array[j-1], array[j]): break` (`sorting.py:40-41`) |
| 한 칸 이동 | `array[j-1], array[j] = array[j], array[j-1]` (`sorting.py:43`) |

## 6. 직접 실행해보기

```bash
python3 -m algorithm.sort.sorting
```

출력의 `insertion sort` 줄을 확인하세요. `bucket_sort`가 각 버킷 정렬에 `insertion_sort`를 재사용하는 부분(`sorting.py:257`)도 함께 살펴보면, 왜 "작은 구간을 빠르게 정렬하는 용도"로 삽입 정렬이 자주 선택되는지 이해할 수 있습니다.

---

[← 이전 문서: SELECTION_SORT.md](./SELECTION_SORT.md) | [목차: README.md](./README.md) | 다음 문서: [SHELL_SORT.md →](./SHELL_SORT.md)
