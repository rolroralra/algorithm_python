# 정렬 알고리즘 (Sorting Algorithms)

> 구현: [`sorting.py`](./sorting.py) — `Sort` 클래스
> 관련 테스트: [`tests/sort/test_sorting.py`](../../tests/sort/test_sorting.py)

## 1. 왜 정렬 알고리즘을 여러 개 알아야 하는가?

파이썬에는 이미 `sorted()`, `list.sort()`라는 매우 빠른 내장 정렬(Timsort)이 있습니다. 그런데도 정렬 알고리즘을 직접 구현해보고 공부하는 이유는, **"데이터의 특성에 따라 최적의 정렬 방법이 다르기 때문"** 입니다.

- 데이터가 거의 정렬되어 있다면? → 삽입 정렬이 `O(n)`에 가깝게 빠름
- 값의 범위가 좁은 정수라면? → 카운팅/라딕스 정렬이 비교조차 없이 `O(n)`에 끝남
- 메모리가 빠듯하다면? → 힙 정렬이 추가 메모리 `O(1)`로 `O(n log n)`을 보장
- 같은 값의 원래 순서를 유지해야 한다면(안정 정렬)? → 병합/카운팅/라딕스 정렬을 선택해야 함

이 디렉토리는 아래 10가지 정렬 알고리즘을 모두 `Sort` 클래스의 static/class 메서드로 구현하고, 각 알고리즘이 "왜 그런 시간복잡도를 갖는지", "왜 안정적이거나 불안정한지"를 코드 레벨에서 설명합니다.

## 2. 문서 목차

정렬 알고리즘을 "비교 기반 단순 정렬 → 비교 기반 고급 정렬 → 비교 기반이 아닌 정렬" 순서로 읽는 것을 권장합니다.

| 순서 | 문서 | 알고리즘 | 분류 |
|---|---|---|---|
| 1 | [BUBBLE_SORT.md](./BUBBLE_SORT.md) | 버블 정렬 | 비교 기반 · 단순 |
| 2 | [SELECTION_SORT.md](./SELECTION_SORT.md) | 선택 정렬 | 비교 기반 · 단순 |
| 3 | [INSERTION_SORT.md](./INSERTION_SORT.md) | 삽입 정렬 | 비교 기반 · 단순 |
| 4 | [SHELL_SORT.md](./SHELL_SORT.md) | 쉘 정렬 | 비교 기반 · 단순의 개선 |
| 5 | [MERGE_SORT.md](./MERGE_SORT.md) | 병합 정렬 | 비교 기반 · 분할 정복 |
| 6 | [QUICK_SORT.md](./QUICK_SORT.md) | 퀵 정렬 | 비교 기반 · 분할 정복 |
| 7 | [HEAP_SORT.md](./HEAP_SORT.md) | 힙 정렬 | 비교 기반 · 자료구조 활용 |
| 8 | [COUNTING_SORT.md](./COUNTING_SORT.md) | 카운팅 정렬 | 비비교 기반 · 분배 |
| 9 | [RADIX_SORT.md](./RADIX_SORT.md) | 라딕스 정렬 | 비비교 기반 · 분배 |
| 10 | [BUCKET_SORT.md](./BUCKET_SORT.md) | 버킷 정렬 | 분배 + 비교 혼합 |

각 문서 하단에는 "이전 문서 | 다음 문서" 링크가 있어서 순서대로 읽어나갈 수 있습니다.

## 3. 한눈에 보는 비교표

| 알고리즘 | 최선 | 평균 | 최악 | 추가 공간 | 안정(Stable)? | 비교 기반? |
|---|---|---|---|---|---|---|
| 버블 정렬 | `O(n)` | `O(n²)` | `O(n²)` | `O(1)` | ✅ 안정 | ✅ |
| 선택 정렬 | `O(n²)` | `O(n²)` | `O(n²)` | `O(1)` | ❌ 불안정 | ✅ |
| 삽입 정렬 | `O(n)` | `O(n²)` | `O(n²)` | `O(1)` | ✅ 안정 | ✅ |
| 쉘 정렬 | `O(n log n)` | 간격 수열에 따라 다름(예: `O(n^1.3)`) | `O(n²)` | `O(1)` | ❌ 불안정 | ✅ |
| 병합 정렬 | `O(n log n)` | `O(n log n)` | `O(n log n)` | `O(n)` | ✅ 안정 | ✅ |
| 퀵 정렬 | `O(n log n)` | `O(n log n)` | `O(n²)` | `O(log n)`(재귀 스택) | ❌ 불안정 | ✅ |
| 힙 정렬 | `O(n log n)` | `O(n log n)` | `O(n log n)` | `O(1)` | ❌ 불안정 | ✅ |
| 카운팅 정렬 | `O(n + k)` | `O(n + k)` | `O(n + k)` | `O(n + k)` | ✅ 안정 | ❌ |
| 라딕스 정렬 | `O(d·(n + b))` | `O(d·(n + b))` | `O(d·(n + b))` | `O(n + b)` | ✅ 안정 | ❌ |
| 버킷 정렬(이 구현체) | `O(n + k)` | `O(n + k)` | `O(n²)`(한 버킷에 몰릴 때) | `O(n + k)` | ✅ 안정 | ⚠️ 조건부(아래 참고) |

`n`은 원소 개수, `k`는 값의 범위, `b`는 라딕스 정렬의 진법(base), `d`는 자릿수(digit) 개수입니다.

모든 구현은 `array[:] = ...` 또는 swap 방식으로 **원본 리스트를 직접 수정(in-place)** 합니다. 다만 `sort()` 통합 메서드는 항상 입력 배열을 `.copy()`한 뒤 정렬하므로 원본이 바뀌지 않습니다(`sorting.py:282`, `sorting.py:291`).

## 4. `comp` (comparator) 파라미터의 의미

비교 기반 알고리즘들은 대부분 다음과 같은 시그니처를 가집니다.

```python
def bubble_sort(array, comp=lambda a, b: a > b):
```

`comp(a, b)`가 `True`를 반환한다는 것은 **"a와 b가 원하는 순서와 반대로 놓여있다(swap이 필요하다)"** 는 뜻입니다.

- 기본값 `lambda a, b: a > b` → "a가 b보다 크면 순서가 어긋난 것" → **오름차순** 정렬
- `lambda a, b: a < b`로 뒤집으면 → "a가 b보다 작으면 순서가 어긋난 것" → **내림차순** 정렬

이 규칙 덕분에 `comp`만 바꿔주면 하나의 정렬 로직으로 오름차순/내림차순은 물론, 커스텀 객체의 필드 기준 정렬까지 모두 지원할 수 있습니다(예: `tests/sort/test_sorting.py:37`).

## 5. `sort()` 통합 진입점의 알고리즘 선택 전략

`Sort.sort()`(`sorting.py:264`)는 "이 알고리즘이 comparator를 받는지"를 함수 시그니처를 직접 조사(`inspect`)해서 자동으로 판단합니다.

```python
params = list(inspect.signature(algorithm).parameters)

if len(params) >= 2 and params[1] == 'comp':
    return cls.__sort_with_comparison(array, comp, algorithm)

return cls.__sort_without_comparison(array, algorithm)
```

- `inspect.signature(algorithm).parameters`로 전달된 `algorithm` 함수의 파라미터 이름 목록을 가져옵니다.
- **두 번째 파라미터 이름이 정확히 `'comp'`인지** 검사합니다.
  - `bubble_sort(array, comp=...)`, `selection_sort(array, comp=...)`, `heap_sort(array, comp=...)`, `bucket_sort(array, comp=...)` 등은 모두 두 번째 파라미터가 `comp` → 비교 기반 경로(`__sort_with_comparison`, `sorting.py:278`)로 가서 `algorithm(cloned_array, comp)` 형태로 호출됩니다.
  - `counting_sort(array)`는 파라미터가 1개뿐이고, `radix_sort(array, base=10)`은 두 번째 파라미터 이름이 `'base'`이지 `'comp'`가 아닙니다 → 비비교 경로(`__sort_without_comparison`, `sorting.py:287`)로 가서 `algorithm(cloned_array)` 형태로, `comp` 없이 호출됩니다.
- 두 경로 모두 공통적으로 **입력 배열을 복사(`.copy()`)한 뒤** 정렬하므로 `sort()`는 원본을 건드리지 않는 순수 함수처럼 동작합니다.

즉 `Sort.sort()`는 "정렬 로직"과 "정렬 알고리즘을 어떻게 호출할지 판단하는 로직"을 분리한 매우 얇은 디스패처(dispatcher)입니다. 새 정렬 알고리즘을 추가할 때도 `sort()` 자체를 수정할 필요 없이, 시그니처 규칙(`(array, comp=...)` 또는 `(array, ...)`)만 지키면 자동으로 인식됩니다.

```python
# 기본 알고리즘은 퀵 정렬(quick_sort)
Sort.sort([3, 1, 2])                                    # [1, 2, 3]

# comparator를 바꾸면 내림차순
Sort.sort([3, 1, 2], comp=lambda a, b: a < b)            # [3, 2, 1]

# algorithm을 바꾸면 다른 정렬 알고리즘 사용
Sort.sort([3, 1, 2], algorithm=Sort.counting_sort)       # [1, 2, 3]
```

## 6. 직접 실행해보기

```bash
python3 -m algorithm.sort.sorting
```

`sorting.py:306`의 `__main__` 블록이 실행되며, 무작위로 생성한 배열 하나를 10가지 알고리즘으로 각각 정렬해 결과를 나란히 출력합니다. 모든 줄의 결과가 서로 같아야 정상입니다.

## 7. 다음 문서

[BUBBLE_SORT.md](./BUBBLE_SORT.md)에서부터 순서대로 읽어보세요.
