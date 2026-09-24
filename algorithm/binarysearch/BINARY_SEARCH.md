# 이진 탐색 (Binary Search)

> 구현: [`binarysearch.py`](./binarysearch.py) — `binarysearch()`
> [`lower_bound.py`](./lower_bound.py) — `lower_bound()`, [`upper_bound.py`](./upper_bound.py) — `upper_bound()`
> 세 파일 모두 "정렬된 배열에서 원하는 위치를 `O(log n)`에 찾는다"는 같은 아이디어를 조금씩 다른 목적에 응용한 것이라 하나의 문서로 묶었습니다.

## 1. 왜 이진 탐색이 필요한가?

정렬되지 않은 배열에서 특정 값을 찾으려면 처음부터 끝까지 하나씩 비교하는 **선형 탐색(linear search)** 밖에 방법이 없습니다. 값 하나를 찾는 데 최악의 경우 배열 크기만큼, 즉 `O(n)`이 걸립니다.

하지만 배열이 **정렬되어 있다면** 훨씬 똑똑하게 찾을 수 있습니다. 가운데 값 하나만 확인해도 "찾는 값이 왼쪽 절반에 있는지, 오른쪽 절반에 있는지"를 즉시 알 수 있기 때문입니다. 매번 탐색 범위를 절반으로 줄여나가면, `n`개의 원소 중에서 원하는 값을 찾는 데 `O(log n)`번의 비교만으로 충분합니다.

```
n = 1,000,000 이어도
log2(1,000,000) ≈ 20

선형 탐색: 최악의 경우 1,000,000번 비교
이진 탐색: 최악의 경우      20번 비교
```

이것이 `binarysearch.py`가 하는 일입니다. `lower_bound.py`/`upper_bound.py`는 여기서 한 걸음 더 나아가, "같은 값이 여러 번 등장할 때 그 구간의 경계를 찾는" 이진 탐색의 대표적인 응용입니다 (C++ STL의 `lower_bound`/`upper_bound`, Python `bisect` 모듈과 동일한 개념).

## 2. 기본 이진 탐색: `binarysearch()`

`binarysearch.py:1`의 `binarysearch(sorted_array, target_value, recursive=False)`는 반복문 버전(`__binarysearch`, `binarysearch.py:7-21`)과 재귀 버전(`__binarysearch_by_recursive`, `binarysearch.py:24-35`) 두 가지를 모두 제공합니다. `recursive` 플래그로 어떤 걸 쓸지 고를 수 있습니다.

두 버전 모두 로직은 동일합니다. `start_index`, `end_index`로 탐색 범위를 표현하고, 매 단계마다 가운데 `mid_index`를 확인합니다.

```python
# binarysearch.py:11-19 (반복문 버전)
while start_index <= end_index:
    mid_index = (start_index + end_index) // 2

    if sorted_array[mid_index] == target_value:
        return mid_index
    elif sorted_array[mid_index] < target_value:
        start_index = mid_index + 1   # 왼쪽 절반은 버림
    else:
        end_index = mid_index - 1     # 오른쪽 절반은 버림
```

### 탐색 과정 시각화

`[1, 3, 5, 7, 9]`에서 `7`을 찾는 과정:

```
index:   0  1  2  3  4
array:   1  3  5  7  9

1단계) start=0, end=4, mid=2 → arr[2]=5 < 7 → start=3
                 ↓
        1  3  [5] 7  9      5 < 7 이므로 왼쪽 절반 버림

2단계) start=3, end=4, mid=3 → arr[3]=7 == 7 → 발견! index 3 반환
                       ↓
        1  3  5  [7]  9
```

한 번 비교할 때마다 탐색 범위가 절반으로 줄어드는 것이 핵심입니다.

## 3. 못 찾았을 때: 음수 인코딩으로 삽입 위치 알려주기

값을 못 찾으면 `binarysearch()`는 단순히 `-1`을 반환하지 않고, `-(start_index + 1)`(`binarysearch.py:21`, `26`)을 반환합니다. 이렇게 하면:

- 반환값이 `0` 이상이면 → 값을 찾았고, 그 인덱스가 곧 위치
- 반환값이 음수면 → 값이 없고, `-(반환값 + 1)`이 **그 값이 들어가야 할 삽입 위치**

`[1, 3, 5, 7, 9]`에서 `4`를 찾는 경우:

```
index:   0  1  2  3  4
array:   1  3  5  7  9

1단계) start=0, end=4, mid=2 → arr[2]=5 > 4 → end=1
2단계) start=0, end=1, mid=0 → arr[0]=1 < 4 → start=1
3단계) start=1, end=1, mid=1 → arr[1]=3 < 4 → start=2
4단계) start=2, end=1        → start > end, 루프 종료

반환값 = -(start_index + 1) = -(2 + 1) = -3
삽입 위치 = -(반환값 + 1) = -(-3 + 1) = 2

즉, 4는 index 2 자리(5 앞)에 들어가야 정렬 순서가 유지됨:
1  3  [4]  5  7  9
```

이 트릭은 Java의 `Collections.binarySearch()`와 동일한 관례입니다 — "찾았다/못 찾았다"와 "못 찾았으면 어디에 넣어야 하는가"를 반환값 하나로 함께 표현할 수 있습니다.

## 4. `lower_bound` / `upper_bound`: 값이 여러 번 등장할 때

일반 이진 탐색은 값이 여러 개 있을 때 그중 **어떤 인덱스**가 반환될지 보장하지 않습니다 (구현에 따라 다름). 반면 `lower_bound`/`upper_bound`는 항상 **경계**를 정확히 짚어줍니다.

- `lower_bound(array, target)` (`lower_bound.py:1`): target **이상**인 첫 번째 위치 (target이 처음 등장하는 자리)
- `upper_bound(array, target)` (`upper_bound.py:1`): target**보다 큰** 첫 번째 위치 (target이 마지막으로 등장한 바로 다음 자리)

```
값:      1   2   2   2   3
인덱스:  0   1   2   3   4
             ↑           ↑
      lower_bound(2)=1   upper_bound(2)=4

[lower_bound, upper_bound) 구간 = target과 같은 값들이 모여 있는 구간
개수 = upper_bound(2) - lower_bound(2) = 4 - 1 = 3개
```

### 코드 한 줄 차이로 갈리는 두 함수

두 함수의 반복문 구조는 완전히 동일하고, **조건문 하나(`<` vs `<=`)만** 다릅니다.

```python
# lower_bound.py:21  — "이상"을 찾음
if sorted_array[mid_index] < target_value:
    start_index = mid_index + 1
else:
    end_index = mid_index - 1
    result = mid_index

# upper_bound.py:21  — "초과"를 찾음
if sorted_array[mid_index] <= target_value:   # 같아도 오른쪽으로 계속 진행
    start_index = mid_index + 1
else:
    end_index = mid_index - 1
    result = mid_index
```

`lower_bound`는 `mid` 값이 target과 **같아도** "더 왼쪽에 후보가 있을 수 있다"고 보고 `end_index`를 줄이며 계속 왼쪽을 탐색합니다. `upper_bound`는 한 걸음 더 나아가, `mid` 값이 target과 같을 때도 "아직 target 구간 안"이라고 보고 **오른쪽으로 계속 전진**(`start_index = mid_index + 1`)해서 target 구간을 지나칠 때까지 찾습니다. 이 작은 차이가 "첫 등장 위치"와 "마지막 등장 위치 + 1"을 가릅니다.

두 함수 모두 값을 못 찾아도 예외 없이 항상 `0`부터 `len(array)` 사이의 유효한 삽입 위치를 반환합니다 (Python `bisect.bisect_left`/`bisect.bisect_right`와 동일한 동작이며, 테스트에서도 이를 직접 비교 검증합니다).

## 5. 시간/공간복잡도

| 연산 | 시간복잡도 | 공간복잡도 |
|---|---|---|
| `binarysearch()` (반복문) | `O(log n)` | `O(1)` |
| `binarysearch()` (재귀) | `O(log n)` | `O(log n)` (호출 스택) |
| `lower_bound()` | `O(log n)` | `O(1)` |
| `upper_bound()` | `O(log n)` | `O(1)` |

## 6. 개념 ↔ 코드 대응표

| 개념 | 코드 위치 |
|---|---|
| 진입점 (반복/재귀 선택) | `binarysearch()` (`binarysearch.py:1`) |
| 반복문 버전 | `__binarysearch()` (`binarysearch.py:7`) |
| 재귀 버전 | `__binarysearch_by_recursive()` (`binarysearch.py:24`) |
| 못 찾았을 때 음수 인코딩 | `-(start_index + 1)` (`binarysearch.py:21`, `26`) |
| "target 이상"의 첫 위치 | `lower_bound()` (`lower_bound.py:1`) |
| "target 초과"의 첫 위치 | `upper_bound()` (`upper_bound.py:1`) |
| lower/upper를 가르는 조건문 | `lower_bound.py:21` (`<`) vs `upper_bound.py:21` (`<=`) |

## 7. pytest로 동작 확인하기

세 파일 모두 `if __name__ == '__main__':` 데모는 없지만, 테스트를 실행하면 동작을 바로 확인할 수 있습니다. `lower_bound`/`upper_bound`는 표준 라이브러리 `bisect.bisect_left`/`bisect.bisect_right`와 결과를 비교하는 랜덤 테스트도 포함되어 있습니다.

```bash
pytest tests/binarysearch/test_binarysearch.py -v
pytest tests/binarysearch/test_lower_bound.py -v
pytest tests/binarysearch/test_upper_bound.py -v
```

---

[◀ 이전: README](./README.md) | [다음: 이진 트리 ▶](./BINARY_TREE.md)
