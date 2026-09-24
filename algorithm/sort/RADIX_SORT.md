# 라딕스 정렬 (Radix Sort)

> 구현: [`sorting.py`](./sorting.py) — `Sort.radix_sort()` (`sorting.py:179`), 내부 헬퍼 `Sort.__counting_sort_by_digit()` (`sorting.py:201`)
> 이전 문서: [COUNTING_SORT.md](./COUNTING_SORT.md) · 목차: [README.md](./README.md)

## 1. 왜 이 알고리즘이 필요한가?

카운팅 정렬은 값의 범위 `k`가 커지면(`sorting.py:155-156`에서 `1,000,000`을 넘으면 아예 예외를 던질 만큼) 급격히 비효율적이 됩니다. `802`처럼 큰 값 하나만 섞여 있어도 범위 전체(`0~802`)만큼의 `count` 배열이 필요하기 때문입니다.

라딕스 정렬은 **"값 전체를 한 번에 비교하지 말고, 자릿수(digit)별로 나눠서 카운팅 정렬을 여러 번 적용하자"** 는 아이디어로 이 문제를 해결합니다. 각 자릿수는 `0~9`(10진법 기준) 사이의 값만 가지므로, 매번 아주 작은 범위(`k = base`, 예: 10)에 대해서만 카운팅 정렬을 수행하면 됩니다. 값 자체가 아무리 커도 **자릿수 개수(`d`)** 만큼만 반복하면 되므로, 큰 범위의 정수도 효율적으로 정렬할 수 있습니다.

## 2. 핵심 아이디어: 가장 낮은 자릿수부터, 안정 정렬을 반복 적용(LSD Radix Sort)

`[170, 45, 802, 24]`를 정렬해봅시다. (LSD = Least Significant Digit, 가장 낮은 자릿수부터 처리)

```
1의 자리(place_value=1) 기준으로 안정 정렬:
  170(0), 45(5), 802(2), 24(4)
  → [170, 802, 24, 45]     (0 < 2 < 4 < 5 순)

10의 자리(place_value=10) 기준으로 안정 정렬:
  170(7), 802(0), 24(2), 45(4)
  → [802, 24, 170, 45]     (0 < 2 < 4 < 7 순)

100의 자리(place_value=100) 기준으로 안정 정렬:
  802(8), 24(0), 170(1), 45(0)
  → [24, 45, 170, 802]     (0(24) < 0(45) < 1 < 8 순)
                    ↑
       24와 45는 100의 자리가 둘 다 0으로 "동점"
       → 안정 정렬이므로 직전 단계(10의 자리)에서 만들어진
         순서(24가 45보다 앞)를 그대로 유지!

최종 결과: [24, 45, 170, 802]  ✅ 정렬 완료
```

**왜 낮은 자릿수부터 정렬해야 할까?** 매 단계에서 "동점(현재 자릿수가 같음)"인 원소들은, 그 이전 단계까지 이미 정해둔 순서를 그대로 유지해야 올바른 결과가 나옵니다. 그래서 각 자릿수를 정렬할 때 반드시 **안정 정렬(stable sort)** 을 써야 하며, 이 구현은 그 역할을 카운팅 정렬로 수행합니다.

## 3. 코드 살펴보기

### 3-1. 자릿수를 순회하는 바깥 로직 (`radix_sort`)

```python
@classmethod
def radix_sort(cls, array, base=10):
    if len(array) <= 1:
        return array

    if base < 2:
        raise ValueError("base must be at least 2.")

    min_val = min(array)
    max_val = max(array)
    max_shifted_value = max_val - min_val

    place_value = 1
    while max_shifted_value // place_value > 0:
        cls.__counting_sort_by_digit(array, min_val, base, place_value)
        place_value *= base

    return array
```

- `base`(`sorting.py:179`): 몇 진법으로 자릿수를 나눌지 지정합니다. 기본값 `10`(십진법). `base`가 `2`보다 작으면 의미가 없으므로 `ValueError`(`sorting.py:183-184`, `tests/sort/test_sorting.py:104-106`에서 검증).
- **음수 지원을 위한 이동(shift)**(`sorting.py:186-188`): `min_val`을 빼서 모든 값을 `0` 이상으로 "이동"시킨 `max_shifted_value`를 계산합니다. 실제 배열 값은 바뀌지 않고, 자릿수 계산 시에만 `(value - min_val)`을 사용합니다 — 이 덕분에 라딕스 정렬이 음수가 섞인 배열도 정상적으로 처리할 수 있습니다(`tests/sort/test_sorting.py:88-90`의 음수 테스트).
- `place_value`(`sorting.py:192`): 현재 보고 있는 자릿수의 자리값(1의 자리=1, 10의 자리=10, 100의 자리=100, ...).
- **반복 조건** `while max_shifted_value // place_value > 0`(`sorting.py:193`): "아직 확인해야 할 자릿수가 남아있는가"를 판단합니다. 가장 큰 값(이동 후 기준)을 `place_value`로 나눈 몫이 `0`이 되면, 더 이상 볼 자릿수가 없다는 뜻이므로 종료합니다.
- 매 반복마다 `__counting_sort_by_digit()`(`sorting.py:195`)으로 "현재 자릿수"만 기준으로 안정 정렬하고, `place_value *= base`(`sorting.py:196`)로 다음 자릿수로 이동합니다.

### 3-2. 자릿수 하나만 보는 카운팅 정렬 (`__counting_sort_by_digit`)

```python
@staticmethod
def __counting_sort_by_digit(array, min_val, base=10, place_value=1):
    size = len(array)
    count = [0] * base
    output = [None] * size

    for value in array:
        digit = ((value - min_val) // place_value) % base
        count[digit] += 1

    for i in range(1, base):
        count[i] += count[i - 1]

    for i in range(size - 1, -1, -1):
        digit = ((array[i] - min_val) // place_value) % base
        count[digit] -= 1
        output[count[digit]] = array[i]

    array[:] = output
```

[COUNTING_SORT.md](./COUNTING_SORT.md)에서 본 `counting_sort()`와 구조가 거의 동일하지만 결정적인 차이가 있습니다.

- `count = [0] * base`(`sorting.py:203`): `counting_sort()`는 `count` 배열 크기가 "값의 전체 범위(`k`)"였지만, 여기서는 **항상 `base`개(기본 10개)** 뿐입니다. 이것이 라딕스 정렬이 큰 범위의 값도 효율적으로 다룰 수 있는 이유입니다.
- `digit = ((value - min_val) // place_value) % base`(`sorting.py:208`, `217`): 값에서 `min_val`을 빼 이동시킨 뒤, `place_value`로 나누고 `base`로 나머지 연산을 해서 "현재 보고 있는 자릿수 하나"만 추출합니다.
  - 예: `value=802`, `min_val=0`, `place_value=100`, `base=10`이면 `(802 // 100) % 10 = 8 % 10 = 8` → 백의 자리 숫자 `8`.
- 나머지 로직(개수 세기 → 누적합 → **원본을 역순으로 순회하며 배치**)은 `counting_sort()`와 완전히 동일한 패턴이며, 동일한 이유로 **안정성**을 보장합니다(`sorting.py:216-219`).
- `array[:] = output`(`sorting.py:221`)으로 이번 자릿수 기준 정렬 결과를 원본에 즉시 반영한 뒤, 다음 자릿수 패스에서 이 결과를 다시 입력으로 사용합니다.

## 4. 시간복잡도 / 공간복잡도 / 안정성

| 항목 | 값 | 설명 |
|---|---|---|
| 최선(Best) | `O(d · (n + b))` | `d`=자릿수 개수, `n`=원소 개수, `b`=진법(`base`) |
| 평균(Average) | `O(d · (n + b))` | |
| 최악(Worst) | `O(d · (n + b))` | 값의 범위와 무관하게 자릿수 개수 `d`에만 의존 |
| 공간(Space) | `O(n + b)` | `__counting_sort_by_digit`가 매 패스마다 만드는 `count`(크기 `b`), `output`(크기 `n`) |
| 안정성(Stable) | ✅ 안정 | 각 자릿수 패스가 카운팅 정렬(안정 정렬)이고, 안정 정렬을 반복 적용하면 전체도 안정적이기 때문 |

카운팅 정렬과 비교하면: 카운팅 정렬의 공간/시간은 값의 범위 `k`에 정비례(`O(n+k)`)하지만, 라딕스 정렬은 값의 **자릿수 개수** `d = log_base(k)`에 비례합니다. `k`가 매우 클 때(`k = 10^9`처럼) 카운팅 정렬은 사용이 불가능하지만(메모리 폭발), 라딕스 정렬은 `d`(약 10)번의 패스만으로 처리할 수 있습니다.

## 5. 개념 ↔ 코드 대응표

| 개념 | 코드 위치 |
|---|---|
| 진법(base) 유효성 검증 | `if base < 2: raise ValueError` (`sorting.py:183-184`) |
| 음수 지원을 위한 값 이동 | `max_shifted_value = max_val - min_val` (`sorting.py:188`) |
| 처리할 자릿수가 남았는지 판단 | `while max_shifted_value // place_value > 0` (`sorting.py:193`) |
| 자릿수 하나 추출 | `((value - min_val) // place_value) % base` (`sorting.py:208`, `217`) |
| 다음 자릿수로 이동 | `place_value *= base` (`sorting.py:196`) |
| 자릿수별 안정 정렬(카운팅 정렬 재사용) | `__counting_sort_by_digit()` (`sorting.py:201`) |

## 6. 직접 실행해보기

```bash
python3 -m algorithm.sort.sorting
```

출력의 `radix sort` 줄을 확인하세요. 잘못된 `base` 값이 거부되는지는 `test_radix_sort_rejects_invalid_base`(`tests/sort/test_sorting.py:104-106`)에서, 음수가 섞인 배열이 올바르게 처리되는지는 `test_array_with_negative_numbers`(`tests/sort/test_sorting.py:88-90`)에서 확인할 수 있습니다.

---

[← 이전 문서: COUNTING_SORT.md](./COUNTING_SORT.md) | [목차: README.md](./README.md) | 다음 문서: [BUCKET_SORT.md →](./BUCKET_SORT.md)
