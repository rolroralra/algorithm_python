# 힙 정렬 (Heap Sort)

> 구현: [`sorting.py`](./sorting.py) — `Sort.heap_sort()` (`sorting.py:143`), 실제 로직은 [`algorithm/heap/heap.py`](../heap/heap.py)의 `Heap.heap_sort()`에 위임
> 이전 문서: [QUICK_SORT.md](./QUICK_SORT.md) · 목차: [README.md](./README.md)

## 1. 왜 이 알고리즘이 필요한가?

퀵 정렬은 평균적으로 빠르지만 최악의 경우 `O(n²)`로 느려질 위험이 있고, 병합 정렬은 항상 `O(n log n)`을 보장하지만 `O(n)`의 추가 메모리가 필요합니다.

힙 정렬은 **"항상 `O(n log n)`을 보장하면서도, 이론적으로는 추가 메모리 `O(1)`만으로 정렬할 수 있다"** 는 것이 가장 큰 장점입니다. **힙(heap)** 이라는 자료구조 — "루트에 항상 최솟값(또는 최댓값)이 위치하는 완전 이진 트리" — 의 성질을 이용해, "가장 작은 값을 꺼내고, 다시 정리하고, 또 꺼내고"를 반복하는 방식입니다.

## 2. 핵심 아이디어: 힙에서 최솟값을 반복해서 꺼내기

이 저장소의 `Heap` 클래스(`algorithm/heap/heap.py`)는 배열 하나로 힙을 표현합니다. 인덱스 `i`의 자식은 `2i+1`, `2i+2`에 위치합니다.

```
배열: [1, 3, 8, 5]

트리로 그리면:
              1            ← 루트 = 이 힙의 최솟값(min-heap)
            /   \
           3     8
          /
         5
```

힙 정렬은 다음 두 단계로 이루어집니다.

1. **힙 만들기(heapify)**: 입력 배열 전체를 한 번에 힙 구조로 재배치합니다. (`Heap.__init__` → `_heapify_bottom_up()`, `heap.py:9-11`, `29-30`)
2. **반복해서 꺼내기(pop)**: 루트(최솟값)를 꺼내고, 마지막 원소를 루트로 옮긴 뒤 다시 힙 모양을 복구(sift-down)하는 과정을 배열이 빌 때까지 반복합니다. 꺼낸 순서대로 나열하면 그대로 정렬된 결과가 됩니다.

```
[1, 3, 8, 5] 에서 pop 반복:

pop 1 → 1을 꺼냄, 나머지 재구성 → [3, 5, 8]
pop 2 → 3을 꺼냄, 나머지 재구성 → [5, 8]
pop 3 → 5를 꺼냄, 나머지 재구성 → [8]
pop 4 → 8을 꺼냄

꺼낸 순서: 1, 3, 5, 8  ← 오름차순으로 정렬됨!
```

## 3. `Heap`의 `comp`도 Sort의 `comp`와 같은 의미

`Heap`의 `compare_function`(기본값 `lambda a, b: a > b`)도 다른 정렬 알고리즘들의 `comp`와 동일하게 **"두 값의 순서가 뒤바뀌어 있는지"** 를 판단합니다. 힙에서는 "부모가 자식보다 뒤에 있어야 하는가"로 해석됩니다.

- 기본값 `a > b`를 쓰면 "부모가 자식보다 크면 순서가 어긋난 것"이라는 규칙이 강제되어 **부모 ≤ 자식**을 항상 만족하는 **최소 힙(min-heap)** 이 만들어집니다 → `pop()`이 매번 최솟값을 반환 → **오름차순** 정렬.
- `comp`를 `a < b`로 뒤집으면 반대로 **최대 힙(max-heap)** 이 되어 `pop()`이 매번 최댓값을 반환 → **내림차순** 정렬.

즉 `Sort`의 다른 알고리즘들처럼, 힙 정렬도 `comp` 하나만 바꾸면 오름차순/내림차순을 자유롭게 뒤집을 수 있습니다.

## 4. 코드 살펴보기

```python
# sorting.py:142-144
@staticmethod
def heap_sort(array, comp=lambda a, b: a > b):
    Heap.heap_sort(array, comp)
```

`Sort.heap_sort()`는 직접 힙 로직을 구현하지 않고, 이미 만들어진 `Heap` 클래스에 그대로 위임합니다. 실제 정렬은 `algorithm/heap/heap.py`의 다음 부분에서 일어납니다.

```python
# heap.py:129-132
@staticmethod
def heap_sort(input_array, comp=lambda a, b: a > b):
    heap_instance = Heap(input_array.copy(), comp)
    for i in range(len(input_array)):
        input_array[i] = heap_instance.pop()
```

- `Heap(input_array.copy(), comp)`: 입력 배열을 **복사**한 뒤 새 `Heap` 인스턴스를 만듭니다. 생성자 내부에서 `_heapify_bottom_up()`(`heap.py:29-30`)이 호출되어 `O(n)`에 힙 구조를 완성합니다.
- `for i in range(len(input_array)): input_array[i] = heap_instance.pop()`: 힙에서 하나씩 꺼내(`pop()`, `heap.py:17-24`) **원본 배열의 앞에서부터** 채워 넣습니다. `pop()`은 루트를 반환값으로 저장한 뒤, 마지막 원소를 루트 자리로 옮기고 `_sift_down()`으로 힙 모양을 복구하는 과정을 `O(log n)`에 수행합니다.

## 5. 구현상의 특이 사항 — 이론적 `O(1)` 공간이지만 실제로는 `O(n)`

교과서적인 힙 정렬은 별도의 배열 없이 **입력 배열 자체를 힙으로 사용**하고, "루트와 마지막 원소를 swap한 뒤 힙 크기를 하나 줄이는" 방식으로 완전히 제자리(in-place)에서 동작해 추가 공간이 `O(1)`입니다.

하지만 이 구현체는 `Heap(input_array.copy(), comp)`(`heap.py:131`)에서 보듯 **입력 배열을 복사해 별도의 `Heap` 객체를 만들고**, 다시 그 결과를 원본 배열에 한 칸씩 써넣는 방식을 씁니다. 정렬 결과는 원본 배열에 반영되어 "겉보기엔 in-place"처럼 보이지만, 내부적으로는 원본 크기만큼의 **추가 배열을 하나 더 사용**하므로 공간복잡도는 `O(1)`이 아니라 `O(n)`입니다. 힙 정렬을 공부할 때 흔히 "`O(1)` 공간"이라고 배우지만, 실제 구현은 이렇게 트레이드오프(코드 단순성 vs 메모리 최적화)를 선택할 수 있다는 점을 보여주는 좋은 예시입니다.

## 6. 시간복잡도 / 공간복잡도 / 안정성

| 항목 | 값 | 설명 |
|---|---|---|
| 최선(Best) | `O(n log n)` | 힙 구조 특성상 데이터 상태와 무관 |
| 평균(Average) | `O(n log n)` | 힙 생성 `O(n)` + `pop` n번 × `O(log n)` |
| 최악(Worst) | `O(n log n)` | 병합 정렬과 마찬가지로 최악의 경우도 보장됨 |
| 공간(Space) | 이론상 `O(1)`, **이 구현체는 `O(n)`** | `input_array.copy()`로 별도 배열 생성(`heap.py:131`) |
| 안정성(Stable) | ❌ 불안정 | `pop()`이 "마지막 원소를 루트로 옮기고 sift-down"하는 과정에서 멀리 떨어진 원소끼리 swap되므로, 같은 값의 상대적 순서가 보존되지 않음 |

## 7. 개념 ↔ 코드 대응표

| 개념 | 코드 위치 |
|---|---|
| `Sort`에서 `Heap`으로 위임 | `Sort.heap_sort()` (`sorting.py:143`) |
| `O(n)` 힙 생성(heapify) | `Heap.__init__` → `_heapify_bottom_up()` (`heap.py:9-11`, `29-30`) |
| 최솟값(루트) 꺼내기 + 힙 재구성 | `Heap.pop()` (`heap.py:17-24`) |
| 힙 정렬 루프 | `Heap.heap_sort()` (`heap.py:129-132`) |
| min-heap ↔ max-heap 전환 | `compare_function` 파라미터 (`heap.py:2`) |

## 8. 직접 실행해보기

```bash
python3 -m algorithm.sort.sorting
```

출력의 `heap sort` 줄을 확인하세요. 힙 자체의 동작(추가/삭제/피크)을 더 자세히 보고 싶다면 별도로 다음을 실행할 수 있습니다.

```bash
python3 -m algorithm.heap.heap
```

---

[← 이전 문서: QUICK_SORT.md](./QUICK_SORT.md) | [목차: README.md](./README.md) | 다음 문서: [COUNTING_SORT.md →](./COUNTING_SORT.md)
