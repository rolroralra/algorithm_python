# 힙 (Heap)

> 구현: [`heap.py`](./heap.py) — `Heap` 클래스

## 1. 왜 힙이 필요한가?

"지금까지 넣은 값들 중 가장 작은(혹은 가장 큰) 값을 빠르게 꺼내고 싶다"는 요구는 매우 흔합니다 — 우선순위 큐, 다익스트라 최단 경로, 이벤트 스케줄링, `heap_sort` 등.

이걸 배열로 단순하게 구현하면 둘 중 하나는 느려집니다.

| 자료구조 | 최솟값 찾기 | 삽입 |
|---|---|---|
| 정렬 안 된 배열 | `O(n)` (전부 훑어야 함) | `O(1)` |
| 매번 정렬된 배열 유지 | `O(1)` | `O(n)` (삽입 위치 찾고 밀어넣기) |

**힙(heap)** 은 이 둘 사이의 타협점입니다. "완전히 정렬"까지는 하지 않고, **"루트(root)가 항상 최솟값(또는 최댓값)이다"** 라는 느슨한 규칙만 유지합니다. 그 대가로 최솟값 조회는 `O(1)`, 삽입/삭제는 `O(log n)`에 끝납니다.

## 2. 완전 이진 트리 + 배열

힙은 개념적으로 **완전 이진 트리(complete binary tree)** 입니다 — 마지막 레벨을 제외한 모든 레벨이 꽉 차 있고, 마지막 레벨은 왼쪽부터 순서대로 채워집니다. 이 "빈틈없이 순서대로 채워진다"는 성질 덕분에, 포인터(`left`/`right`) 없이 **배열 하나만으로** 트리를 표현할 수 있습니다.

```
트리 모양:                 배열 표현 (self.array):

         1                index:  0   1   2   3   4   5   6
        / \                       ┌───┬───┬───┬───┬───┬───┬───┐
       3   6               값:    │ 1 │ 3 │ 6 │ 5 │ 9 │ 8 │ 7 │
      / \   \                     └───┴───┴───┴───┴───┴───┴───┘
     5   9   7
```

부모와 자식의 인덱스는 계산만으로 바로 구해집니다 (`heap.py:116-126`):

```python
parent_index(i)      = (i - 1) // 2
left_child_index(i)  = 2 * i + 1
right_child_index(i) = 2 * i + 2
```

예를 들어 인덱스 `2`(값 `6`)의 부모는 `(2-1)//2 = 0`(값 `1`), 자식은 `2*2+1=5`(값 `8`)와 `2*2+2=6`(값 `7`)입니다 — 위 그림과 정확히 일치합니다.

## 3. min-heap vs max-heap: `compare_function`

`Heap`은 힙의 방향(최솟값 우선 / 최댓값 우선)을 하드코딩하지 않고, 생성자에서 `compare_function`을 주입받습니다(`heap.py:2`).

```python
def __init__(self, input_array=None, compare_function=lambda a, b: a > b):
```

`compare_function(x, y)`는 **"x와 y가 지금 순서(부모=x, 자식=y)로 있으면 안 된다"** 를 뜻합니다 — `True`가 나오면 두 값을 swap합니다. 기본값 `a > b`를 쓰면 "부모가 자식보다 크면 잘못된 상태"라고 판단하므로, 결과적으로 **작은 값이 위로 올라가는 min-heap**이 됩니다 (`pop()`이 오름차순으로 값을 내어줌 — `test_default_comparator_pops_ascending`에서 확인). 반대로 `a < b`를 넘기면 큰 값이 위로 올라가는 **max-heap**이 됩니다 (`test_reversed_comparator_pops_descending`).

```
기본 compare_function = (a > b) → min-heap
             1                     pop() 순서: 1, 3, 5, 6, ...
            / \
           3   5
          /
         6

compare_function = (a < b) → max-heap
             9                     pop() 순서: 9, 6, 5, 3, ...
            / \
           6   5
          /
         3
```

## 4. 삽입: `add()` + sift-up

새 값은 일단 배열 맨 끝(트리의 "다음 빈자리")에 追加한 뒤(`heap.py:14`), 부모와 비교하며 **위로 올려보냅니다**(sift-up / bubble-up, `heap.py:38-40`, `55-59`).

```
min-heap에 2 삽입:

     1                    1                    1
    / \                  / \                  / \
   3   5     →  끝에    3   5     → 2 < 3   2   5
  / \           추가   / \          swap    / \
 6   9         2      6   9  2             6   9  3
                                (2가 부모(3)보다 작으므로 교환, 다시 위로 비교 → 1과 비교, 1<2이므로 멈춤)
```

`_sift_up`은 `compare_function(부모, 나)`가 참인 동안(=순서가 잘못된 동안) 부모와 계속 교환하며 루트 방향으로 올라갑니다. 한 번 삽입에 최대 트리 높이(`O(log n)`)만큼 비교/swap이 일어납니다.

## 5. 삭제: `pop()` + sift-down

루트(`array[0]`)가 항상 답이므로 `pop()`은 루트를 반환합니다. 하지만 루트를 그냥 비워두면 트리 모양이 깨지므로, **배열의 마지막 원소를 루트로 옮겨온 뒤**(`heap.py:23`) 그 값을 **아래로 내려보냅니다**(sift-down, `heap.py:42-44`, `78-89`).

```
min-heap에서 pop():

     1                    9  (마지막 원소를 루트로)      3
    / \                  / \                          / \
   3   5      pop() →   3   5       sift-down →      6   5
  / \                  / \                          /
 6   9                6                             9

1단계) 루트=9. 자식(3, 5) 중 더 작은 3과 비교 → 9>3이므로 swap
2단계) 9는 이제 인덱스 1 자리. 자식(6) 중 더 작은 값과 비교 → 9>6이므로 swap
3단계) 더 내려갈 자식이 없으므로 종료
```

`_sift_down`은 매 단계 왼쪽/오른쪽 자식 중 "더 위로 와야 할" 값을 찾아 그 자식과 비교·교환하는 과정을 자식이 없을 때까지 반복합니다. 역시 `O(log n)`.

## 6. 힙 만들기: `_heapify_bottom_up`

배열을 통째로 받아 힙을 만들 때(`heap.py:9-10`), 값을 하나씩 `add()`로 넣으면 `O(n log n)`이 걸립니다. 대신 `Heap`은 **`_heapify_bottom_up`**(`heap.py:30-32`)을 사용합니다 — 마지막 리프의 부모부터 거꾸로 훑으면서, 각 노드에 대해 `_sift_down`만 호출합니다.

```python
for i in range(Heap.parent_index(self._last_index()), -1, -1):
    self._sift_down(i)
```

리프 노드는 sift-down할 필요가 없으므로 건너뛰고, 아래(트리 밑동)에서 위(루트)로 올라가며 "이 부분 트리를 힙 조건에 맞게 정리"하는 작업만 반복합니다. 이렇게 하면 전체 시간이 `O(n)`으로 줄어듭니다 (각 레벨에서 처리할 노드 수와 sift-down 비용이 반비례하기 때문). 참고로 비교용으로 `_heapify_top_down`(`heap.py:34-36`, 값을 하나씩 sift-up)도 코드에 남아있지만 기본적으로는 사용되지 않습니다(`heap.py:11`에서 주석 처리).

## 7. `heap_sort` — 힙을 이용한 정렬

`Heap.heap_sort(input_array, comp=...)`(`heap.py:129-132`)는 입력 배열을 복사해 힙을 만든 뒤, `pop()`을 반복 호출해 나온 값을 원본 배열에 순서대로 덮어씁니다. 기본 비교자(`a > b` → min-heap)를 쓰면 오름차순, `a < b`(max-heap)를 쓰면 내림차순으로 정렬됩니다.

## 8. 시간/공간복잡도

| 연산 | 시간복잡도 | 설명 |
|---|---|---|
| `peek()` / `get_max()` | `O(1)` | 루트를 그냥 읽기만 함 |
| `add()` (삽입) | `O(log n)` | sift-up, 최대 트리 높이만큼 이동 |
| `pop()` (삭제) | `O(log n)` | sift-down, 최대 트리 높이만큼 이동 |
| 배열로부터 힙 생성 (`_heapify_bottom_up`) | `O(n)` | 값을 하나씩 `add()`하는 `O(n log n)`보다 빠름 |
| `heap_sort()` | `O(n log n)` | 힙 생성 `O(n)` + `pop()` n번 × `O(log n)` |
| 공간 | `O(n)` | 배열 하나로 트리 전체를 표현 (포인터 불필요) |

## 9. 개념 ↔ 코드 대응표

| 개념 | 코드 위치 |
|---|---|
| 힙 컨테이너 (배열 + 비교자) | `Heap.__init__` (`heap.py:2`) |
| 부모/왼쪽/오른쪽 자식 인덱스 공식 | `parent_index`, `left_child_index`, `right_child_index` (`heap.py:117`, `121`, `125`) |
| 삽입 (끝에 추가 + 위로 올리기) | `add()` → `_sift_up()` (`heap.py:13`, `38`) |
| 삭제 (루트 교체 + 아래로 내리기) | `pop()` → `_sift_down()` (`heap.py:17`, `42`) |
| 배열 → 힙 변환 (O(n)) | `_heapify_bottom_up()` (`heap.py:30`) |
| min-heap/max-heap 방향 결정 | `compare_function` 매개변수 (`heap.py:2`) |
| 힙을 이용한 정렬 | `heap_sort()` (`heap.py:129`) |

## 10. 직접 실행해보기

```bash
python3 -m algorithm.heap.heap
```

`__main__` 데모(`heap.py:134-161`)에서 기본 min-heap, `compare_function=lambda a, b: a < b`로 만든 max-heap, 그리고 `heap_sort()` 결과를 순서대로 확인할 수 있습니다.

## 관련 테스트

```bash
pytest tests/heap/test_heap.py -v
```
