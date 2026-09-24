# 카운팅 정렬 (Counting Sort)

> 구현: [`sorting.py`](./sorting.py) — `Sort.counting_sort()` (`sorting.py:147`)
> 이전 문서: [HEAP_SORT.md](./HEAP_SORT.md) · 목차: [README.md](./README.md)

## 1. 왜 이 알고리즘이 필요한가?

지금까지 본 알고리즘들은 모두 **두 원소를 서로 비교**(`comp(a, b)`)해서 순서를 정했습니다. 이론적으로, 비교만으로 정렬하는 알고리즘은 아무리 잘 만들어도 `O(n log n)`보다 빠를 수 없다는 것이 증명되어 있습니다(비교 기반 정렬의 하한선).

카운팅 정렬은 **"비교를 아예 하지 않음"** 으로써 이 한계를 뛰어넘습니다. 대신 전제 조건이 있습니다 — **값의 범위(range)를 미리 알아야 하고, 그 범위가 충분히 작아야 합니다.** "값이 몇 번 등장했는지" 세기만 하면, 셈이 끝난 시점에 이미 정렬 순서를 알 수 있다는 아이디어입니다. 예를 들어 시험 점수(0~100점)처럼 값의 범위가 좁고 정수인 데이터에 매우 강력합니다.

## 2. 핵심 아이디어: 값을 세고(count), 누적하고(cumulative), 제자리에 배치

`[4, 2, 4, 1]`을 정렬하는 과정을 따라가봅시다. (구분을 위해 두 개의 `4`를 `4ₐ`, `4_c`로 표기합니다 — `4ₐ`가 원본에서 더 앞에 있습니다.)

### 2-1. 값의 개수 세기 (`count`)

```
원본: [4ₐ, 2, 4_c, 1]   (min=1, max=4)

각 값이 등장한 횟수를 count 배열에 기록 (인덱스 = 값 - min_val)
     값:    1    2    3    4
count : [   1,   1,   0,   2  ]
```

### 2-2. 누적합(cumulative sum)으로 "제자리"를 계산

```
count[i] += count[i-1] 를 누적 적용

     값:    1    2    3    4
count : [   1,   2,   2,   4  ]
              ↑              ↑
        "1 이하인 값"은      "4 이하인 값"은
        1개 있다            4개 있다(즉, 값 4는 정렬 후
                             인덱스 0~3 중 마지막 자리를 채움)
```

이제 `count[value - min_val]`은 **"이 값(포함)까지의 원소가 정렬된 배열에서 몇 번째 자리까지 차지하는가"** 를 의미합니다.

### 2-3. 원본을 거꾸로 훑으며 제자리에 배치 (안정성의 핵심)

```
원본을 뒤에서부터: 1, 4_c, 2, 4ₐ  순서로 처리

1을 처리   → count[0](값1)을 1→0으로 감소 → sorted_array[0] = 1
4_c를 처리 → count[3](값4)을 4→3으로 감소 → sorted_array[3] = 4_c
2를 처리   → count[1](값2)을 2→1로 감소 → sorted_array[1] = 2
4ₐ를 처리 → count[3](값4)을 3→2로 감소 → sorted_array[2] = 4ₐ

결과: [1, 2, 4ₐ, 4_c]
```

`4ₐ`(원본에서 더 앞에 있던 4)가 `4_c`보다 **앞자리**에 배치되었습니다 — 원본에서의 순서가 그대로 유지된 것입니다. 이것이 바로 **"원본 배열을 뒤에서부터(역순으로) 순회"** 하는 이유입니다: 같은 값이 여러 개 있을 때, 더 뒤에 있던 원소를 먼저 처리해 그 값의 "구간" 중 가장 뒤쪽 칸에 배치하면, 자연히 더 앞에 있던 원소가 앞쪽 칸에 배치되어 상대적 순서가 보존됩니다.

## 3. 코드 살펴보기

```python
@staticmethod
def counting_sort(array):
    if len(array) <= 1:
        return array

    min_val = min(array)
    max_val = max(array)
    value_size = max_val - min_val + 1

    if value_size > 1000000:
        raise ValueError("Counting sort is not suitable for large ranges of values.")

    count = [0] * value_size

    for value in array:
        count[value - min_val] += 1

    for i in range(1, value_size):
        count[i] += count[i - 1]

    sorted_array = [None] * len(array)

    for value in reversed(array):
        count[value - min_val] -= 1
        sorted_array[count[value - min_val]] = value

    array[:] = sorted_array
    return array
```

- `comp` 파라미터가 없습니다(`sorting.py:147`). 애초에 원소끼리 크고 작음을 비교하지 않으므로 커스텀 정렬 기준을 줄 수 없습니다 — **오직 오름차순만** 가능합니다.
- `value_size = max_val - min_val + 1`(`sorting.py:153`): 값의 범위. 이 범위 크기만큼 `count` 배열을 만듭니다.
- **안전장치**(`sorting.py:155-156`): 범위가 `1,000,000`을 넘으면 `ValueError`를 발생시킵니다. 예를 들어 `[0, 2_000_000]`처럼 값 2개뿐이어도 범위가 200만이면 `count` 배열을 200만 칸 만들어야 하므로 메모리/시간 낭비가 심해지기 때문입니다(`tests/sort/test_sorting.py:100-102`에서 검증).
- **개수 세기**(`sorting.py:161-162`): 각 값이 몇 번 등장했는지 기록.
- **누적합**(`sorting.py:165-166`): `count[i]`가 "값 `min_val + i` 이하인 원소의 총 개수"가 되도록 변환. 이것이 곧 정렬된 배열에서 그 값이 차지하는 마지막 인덱스(+1)입니다.
- **역순 배치**(`sorting.py:171-173`): `reversed(array)`로 원본을 뒤에서부터 순회하며, 각 값에 해당하는 `count` 칸을 하나 줄이고(`-= 1`) 그 위치에 값을 배치합니다. 앞서 설명한 안정성의 핵심 로직입니다.
- 마지막에 `array[:] = sorted_array`(`sorting.py:175`)로 원본 배열을 직접 갱신하고, 동시에 결과를 `return`도 합니다 — 그래서 `Sort.sort()`를 거치지 않고 `Sort.counting_sort(array)`를 직접 호출해도 반환값을 바로 쓸 수 있습니다.

## 4. 시간복잡도 / 공간복잡도 / 안정성

| 항목 | 값 | 설명 |
|---|---|---|
| 최선(Best) | `O(n + k)` | `n`=원소 개수, `k`=값의 범위(`value_size`) |
| 평균(Average) | `O(n + k)` | 데이터 분포와 무관하게 항상 동일 |
| 최악(Worst) | `O(n + k)` | |
| 공간(Space) | `O(n + k)` | `count` 배열 크기 `k`, `sorted_array` 크기 `n` |
| 안정성(Stable) | ✅ 안정 | 원본을 역순으로 순회하며 배치하는 방식 덕분(2-3절 참고) |

`k`(값의 범위)가 `n`(원소 개수)보다 훨씬 크면 오히려 비효율적입니다 — 예를 들어 원소 10개인데 값의 범위가 100만이면 `O(n + k) ≈ O(k)`가 되어 비교 기반 정렬(`O(n log n)`)보다 느려집니다. 카운팅 정렬은 **"값의 범위가 원소 개수와 비슷하거나 더 작을 때"** 진가를 발휘합니다.

## 5. 개념 ↔ 코드 대응표

| 개념 | 코드 위치 |
|---|---|
| 값의 범위 계산 | `value_size = max_val - min_val + 1` (`sorting.py:153`) |
| 큰 범위에 대한 방어 로직 | `if value_size > 1000000: raise ValueError` (`sorting.py:155-156`) |
| 값별 등장 횟수 집계 | `count[value - min_val] += 1` (`sorting.py:161-162`) |
| 누적합으로 "제자리" 계산 | `count[i] += count[i - 1]` (`sorting.py:165-166`) |
| 안정성을 지키는 역순 배치 | `for value in reversed(array): ...` (`sorting.py:171-173`) |
| 결과를 원본에 반영 | `array[:] = sorted_array` (`sorting.py:175`) |

## 6. 직접 실행해보기

```bash
python3 -m algorithm.sort.sorting
```

출력의 `counting sort` 줄을 확인하세요. 값의 범위가 지나치게 크면 예외가 발생하는지는 `test_counting_sort_rejects_huge_value_range`(`tests/sort/test_sorting.py:100-102`)에서 직접 확인할 수 있습니다.

---

[← 이전 문서: HEAP_SORT.md](./HEAP_SORT.md) | [목차: README.md](./README.md) | 다음 문서: [RADIX_SORT.md →](./RADIX_SORT.md)
