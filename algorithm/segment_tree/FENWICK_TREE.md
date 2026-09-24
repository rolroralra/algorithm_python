# 펜윅 트리 / 이진 인덱스 트리 (Fenwick Tree / Binary Indexed Tree, BIT)

> 구현: [`fenwick_tree/fenwick_tree.py`](./fenwick_tree/fenwick_tree.py) — `FenwickTree` 클래스
> 이 문서를 읽기 전에 [`SEGMENT_TREE.md`](./SEGMENT_TREE.md)를 먼저 읽어두면 "왜 두 자료구조를 비교하는지"가 자연스럽게 이해됩니다.
>
> ⚠️ **읽기 전에**: 이 저장소에는 `binary_index_tree/binary_index_tree.py`라는 파일도 있지만, 코드를 직접 읽어보면 **BIT가 아니라 세그먼트 트리의 또 다른 구현체**입니다. 왜 그런지는 [7절](#7-주의-binary_index_treepy는-사실-bit가-아니다)에서 자세히 설명합니다.

## 1. 왜 펜윅 트리가 필요한가?

[`SEGMENT_TREE.md`](./SEGMENT_TREE.md)에서 본 세그먼트 트리는 구간 합/최솟값/최댓값 등 어떤 결합 법칙(associative) 연산이든 `O(log n)`에 처리할 수 있는 범용 도구입니다. 하지만 그만큼 노드마다 담당 구간(`node_left_index`, `node_right_index`)을 계산해야 하고, 트리 배열도 `4n`에 가까운 크기를 씁니다.

만약 **"구간 합(또는 구간 XOR처럼 '되돌릴 수 있는' 연산)만 필요하다"** 는 제약을 받아들이면, 훨씬 가벼운 구조로 같은 `O(log n)` 성능을 낼 수 있습니다. 이것이 **펜윅 트리(Fenwick Tree)**, 흔히 **BIT(Binary Indexed Tree)** 라고도 부르는 자료구조입니다. 트리를 명시적으로 만드는 대신, **배열 인덱스의 이진수 표현 자체를 트리 구조로 활용**합니다.

## 2. 핵심 도구: `lowbit(i) = i & -i`

BIT의 모든 동작은 한 가지 비트 연산에서 출발합니다 — 어떤 정수 `i`의 **최하위 1비트(lowest set bit)** 만 뽑아내는 `i & -i`입니다.

```
i = 6 = 0b0110
-i (2의 보수)  = 0b...11111010

  0110
& 1010     (하위 비트만 보면)
------
  0010   = 2

즉 lowbit(6) = 2
```

이 값은 항상 `2`의 거듭제곱이고, `fenwick_tree.py`의 `tree[i]`가 **"인덱스 `i`에서 시작해서 왼쪽으로 `lowbit(i)`개만큼의 구간 합"** 을 저장한다는 뜻이 됩니다 — 즉 `tree[i]`는 `array[i - lowbit(i) + 1 ... i]`의 합입니다.

| 인덱스 `i` (이진수) | `lowbit(i)` | `tree[i]`가 담당하는 원본 구간 |
|---|---|---|
| 1 (`0001`) | 1 | `[1, 1]` |
| 2 (`0010`) | 2 | `[1, 2]` |
| 3 (`0011`) | 1 | `[3, 3]` |
| 4 (`0100`) | 4 | `[1, 4]` |
| 5 (`0101`) | 1 | `[5, 5]` |
| 6 (`0110`) | 2 | `[5, 6]` |
| 7 (`0111`) | 1 | `[7, 7]` |
| 8 (`1000`) | 8 | `[1, 8]` |

세그먼트 트리처럼 노드 객체나 `left`/`right` 포인터를 두지 않고도, **인덱스의 이진수 패턴만으로 "누가 어느 구간을 담당하는지"가 정해집니다.** (`fenwick_tree.py`는 1-indexed로 설계되어 있습니다 — `BASE_INDEX = 1`, `fenwick_tree.py:2`.)

## 3. 갱신(`update`): `i += lowbit(i)`로 조상을 따라 올라가기

인덱스 `i`의 값이 바뀌면, `i`를 포함하는 모든 `tree[j]`(`j`가 담당하는 구간이 `i`를 포함하는 경우)를 갱신해야 합니다. 그 `j`들은 `i += (i & -i)`를 반복하면 정확히 얻어집니다(`fenwick_tree.py:24-27`).

```python
def update(self, index, diff):
    while index < self.size:
        self.tree[index] += diff
        index += (index & -index)
```

`n=8`일 때 `update(3, diff)`를 호출하면:

```
3 (0011) → tree[3] += diff       (lowbit=1, 다음: 3+1=4)
4 (0100) → tree[4] += diff       (lowbit=4, 다음: 4+4=8)
8 (1000) → tree[8] += diff       (lowbit=8, 다음: 8+8=16 > size, 종료)

     tree[8]=[1,8]
        ↑
     tree[4]=[1,4]
        ↑
     tree[3]=[3,3]  ← 여기서 시작
```

인덱스 `3`을 포함하는 구간을 담당하는 노드는 딱 `3 → 4 → 8` 이 세 개뿐이고, 트리 전체 높이만큼인 `O(log n)`번만 갱신하면 끝납니다. `fenwick_tree.py`의 `update(index, diff)`는 값을 **덮어쓰는 게 아니라 "차이(diff)만큼 더하는"** 방식이라는 점도 눈여겨볼 부분입니다 (`test_update_adds_diff_instead_of_replacing`에서 검증).

## 4. 조회(`query`): `i -= lowbit(i)`로 내려가며 접두사 합 모으기

내부 헬퍼 `__query(index)`(`fenwick_tree.py:14-21`)는 "인덱스 `1`부터 `index`까지의 합"(접두사 합, prefix sum)을 구합니다. 이번엔 반대로 `i -= (i & -i)`를 반복합니다.

```python
def __query(self, index):
    result = 0
    while index > 0:
        result += self.tree[index]
        index -= (index & -index)
    return result
```

`prefix_sum(6)`을 구하면:

```
6 (0110) → result += tree[6]   (=[5,6]의 합)   다음: 6-2=4
4 (0100) → result += tree[4]   (=[1,4]의 합)   다음: 4-4=0, 종료

tree[6] + tree[4] = sum([5,6]) + sum([1,4]) = sum([1,6])
```

`6`의 이진수 `0110`에서 `1`인 비트가 두 개뿐이라, 딱 두 조각만 더하면 `[1,6]` 전체 합이 나옵니다 — 이 반복 횟수는 항상 `index`의 이진수에서 **`1`인 비트의 개수** 만큼이고, 최대 `O(log n)`입니다.

공개 메서드 `query(start_index, end_index)`(`fenwick_tree.py:10-11`)는 이 접두사 합 두 개의 차로 구간 합을 구합니다 — 누적합 배열과 완전히 같은 아이디어입니다.

```python
def query(self, start_index, end_index):
    return self.__query(end_index) - self.__query(start_index - 1)
```

```
query(2, 4) = prefix_sum(4) - prefix_sum(1)
            = sum([1,4])    - sum([1,1])
            = sum([2,4])
```

## 5. 세그먼트 트리 대비 장단점

| 항목 | 세그먼트 트리 | 펜윅 트리(BIT) |
|---|---|---|
| 지원 연산 | 결합 법칙만 만족하면 무엇이든 (합, 최솟값, 최댓값, ...) | **역원이 있는(invertible)** 연산만 — 합, XOR 등. 최솟값/최댓값은 기본 형태로 불가 |
| 배열 크기 | `O(n)`이지만 계수가 큼 (`~4n`) | `O(n)` (`n+1`), 훨씬 작음 |
| 코드 복잡도 | 재귀 + 구간 분기 로직 필요 | 반복문 + 비트 연산 두 줄이 전부 |
| `update` | 구간을 새 값으로 "대체" (예: `segment_tree.py`) | 기존 값에 "차이"를 더함 (`fenwick_tree.py`) |
| 구간 합을 구하는 방식 | 구간을 `O(log n)`개의 부분 구간으로 분해해 합침 | 접두사 합 두 번(`prefix(r) - prefix(l-1)`)의 차 |

즉 "구간 합만 있으면 된다"는 상황이라면 펜윅 트리가 더 간단하고 가볍습니다. 반대로 구간 최솟값/최댓값처럼 되돌릴 수 없는 연산이 필요하면 세그먼트 트리를 써야 합니다.

## 6. 시간/공간복잡도

| 연산 | 시간복잡도 |
|---|---|
| `update()` | `O(log n)` |
| `query()` (구간 합) | `O(log n)` (내부적으로 접두사 합을 두 번 계산) |
| 공간 | `O(n)` (`self.tree`의 크기는 `size + 1`) |

## 7. 주의: `binary_index_tree.py`는 사실 BIT가 아니다

`algorithm/segment_tree/binary_index_tree/binary_index_tree.py`도 존재하고, 클래스 이름도 폴더 이름도 "BIT"를 가리킵니다. 하지만 실제 코드를 읽어보면:

```python
# binary_index_tree.py:1-31 (요약)
class SegmentTree:                       # ← 클래스 이름부터 SegmentTree
    def __init__(self, capacity=10):
        size = 1
        while size < capacity:
            size *= 2
        size = size * 2 - 1
        self.tree = [0] * size

    def __update(self, index, value, node, node_left_index, node_right_index):
        ...
        node_mid_index = (node_left_index + node_right_index) // 2
        left_node = node * 2 + 1
        right_node = left_node + 1
        self.__update(index, value, left_node, node_left_index, node_mid_index)
        self.__update(index, value, right_node, node_mid_index + 1, node_right_index)
        self.tree[node] = self.tree[left_node] + self.tree[right_node]
```

`i & -i` 같은 비트 연산은 **전혀 등장하지 않고**, `node * 2 + 1` / `node * 2 + 2`로 자식을 찾고 `node_left_index`/`node_right_index` 구간을 재귀로 반씩 나누는 방식은 [`SEGMENT_TREE.md`](./SEGMENT_TREE.md)에서 다룬 `segment_tree.py`와 구조적으로 동일합니다. 즉 **이름과 폴더 위치만 "이진 인덱스 트리"일 뿐, 실제 구현은 (합 연산 전용으로 단순화된) 재귀 세그먼트 트리**입니다.

`segment_tree.py`와 비교했을 때의 차이는 BIT 여부가 아니라 다음 정도입니다:

| 항목 | `segment_tree.py` | `binary_index_tree.py` |
|---|---|---|
| 실제 정체 | 세그먼트 트리 | 세그먼트 트리 (합 연산 전용) |
| 연산자 커스터마이징 | 가능 (`min`, `max`, `operator.add` 등 주입) | 불가 — 덧셈 하드코딩 (`binary_index_tree.py:31`) |
| `update` 시맨틱 | 값 대체 | 값 대체 (동일) |
| 범위를 벗어난 쿼리 | `None`으로 표시 후 상위에서 병합 | `0`(합의 항등원)을 바로 반환 |
| 비트 연산(`i & -i`) 사용 여부 | 없음 | **없음** (BIT라는 이름과 달리) |

**진짜 BIT/펜윅 트리 구현은 `fenwick_tree/fenwick_tree.py`뿐입니다.** 이 문서의 2~6절에서 설명한 `lowbit`/`i & -i` 기반 동작이 바로 그 구현이며, `binary_index_tree.py`는 이름은 같지만 알고리즘적으로는 세그먼트 트리 계열로 분류하는 것이 정확합니다.

## 8. 개념 ↔ 코드 대응표

| 개념 | 코드 위치 |
|---|---|
| 1-indexed 트리 배열 생성 | `FenwickTree.__init__` (`fenwick_tree.py:4`) |
| 최하위 비트 추출 (`lowbit`) | `index & -index` (`fenwick_tree.py:19`, `27`) |
| 값 변경 → 조상 방향으로 전파 | `update()` (`fenwick_tree.py:24-27`) |
| 접두사 합 계산 | `__query()` (`fenwick_tree.py:14-21`) |
| 구간 합 = 접두사 합의 차 | `query()` (`fenwick_tree.py:10-11`) |
| (이름은 같지만) 실제로는 세그먼트 트리인 구현 | `binary_index_tree/binary_index_tree.py` — [7절](#7-주의-binary_index_treepy는-사실-bit가-아니다) 참고 |

## 9. 관련 테스트

```bash
pytest tests/segment_tree/fenwick_tree/test_fenwick_tree.py -v
pytest tests/segment_tree/binary_index_tree/test_binary_index_tree.py -v
```

두 테스트 모두 "무작위 값에 대해 직접 누적합을 구한 결과와 일치하는지" 검증하는 랜덤 테스트를 포함합니다 — `binary_index_tree.py` 쪽 테스트는 `SegmentTree`를 `binary_index_tree.binary_index_tree`에서 import한다는 점(`test_binary_index_tree.py:5`)에서도, 이 구현이 이름과 달리 세그먼트 트리 계열임을 다시 확인할 수 있습니다.

---

[◀ 이전: 세그먼트 트리](./SEGMENT_TREE.md) | [인덱스로 돌아가기 ▶](./README.md)
