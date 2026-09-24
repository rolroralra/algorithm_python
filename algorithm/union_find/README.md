# Union-Find (Disjoint Set Union)

> 구현: [`union_find.py`](./union_find.py) — `UnionFind` 클래스

## 1. 왜 Union-Find가 필요한가?

실생활에서 이런 질문을 자주 마주칩니다.

- "이 두 사람이 같은 친구 그룹에 속해 있나요?"
- "이 두 컴퓨터가 같은 네트워크로 연결되어 있나요?"
- "이 간선을 그래프에 추가하면 사이클(cycle)이 생기나요?"

가장 단순한 방법은 그룹을 리스트로 관리하면서 매번 전체를 뒤지는 것입니다. 그룹이 많고 원소가 많아지면 이 방식은 순식간에 느려집니다.

**Union-Find(합집합-찾기, Disjoint Set Union / DSU)** 는 "서로 겹치지 않는 집합들(disjoint sets)"을 관리하면서, 다음 두 연산을 거의 `O(1)`에 가깝게 처리하는 자료구조입니다.

- `find(x)`: `x`가 속한 집합의 대표(root)가 누구인지 알려준다.
- `union(a, b)`: `a`가 속한 집합과 `b`가 속한 집합을 하나로 합친다.

두 원소가 같은 집합인지는 `find(a) == find(b)`로 즉시 판단할 수 있습니다. 이 성질 덕분에 Union-Find는:

- **사이클 판별**: 간선 `(a, b)`를 추가하기 전에 `find(a) == find(b)`이면, 이미 연결되어 있다는 뜻이므로 이 간선을 추가하면 사이클이 생깁니다.
- **최소 신장 트리(MST) Kruskal 알고리즘**의 핵심 부품으로 쓰입니다. → [mst/README.md](../mst/README.md)
- 친구 관계, 네트워크 연결 컴포넌트, 이미지의 연결 영역(connected component) 관리 등에 두루 쓰입니다.

## 2. 핵심 아이디어: 집합을 "트리"로 표현한다

각 집합을 하나의 트리로 표현하고, 트리의 루트를 그 집합의 "대표"로 삼습니다. 배열 하나(`parent`)로 이 숲(forest) 전체를 표현합니다.

```
parent = [-1, -1, -1, -1, -1]   # 원소 5개, 모두 자기 자신이 루트(집합 크기 1)

0   1   2   3   4     ← 5개의 독립된 집합 (트리 5개, 각각 노드 1개)
```

`union(0, 1)` 을 하면:

```
    0        2   3   4
    |
    1
```

이제 `find(0)`과 `find(1)`은 모두 `0`을 반환합니다.

**코드 연결**: `UnionFind.__init__()`(`union_find.py:2-4`)에서 `self.parent = [-1] * size`로 초기화합니다. 이때 `-1`은 단순히 "루트 표시"가 아니라 "이 집합의 크기가 1"이라는 뜻입니다. 이 인코딩은 아래 4장에서 자세히 설명합니다.

## 3. 최적화 1: Path Compression (경로 압축)

아무 최적화도 하지 않으면 `union`을 계속 한쪽으로만 반복할 때 트리가 일자로 늘어진 연결 리스트가 되어 `find`가 `O(n)`이 될 수 있습니다.

```
union(0,1), union(1,2), union(2,3), union(3,4) 를 최적화 없이 반복하면:

0 → 1 → 2 → 3 → 4     find(0) 하려면 4번 타고 올라가야 함
```

**경로 압축**은 `find`로 루트를 찾아 올라가는 길에 지나친 모든 노드를, 그 루트에 바로 매달아버리는 기법입니다.

```
find(0) 호출 전:          find(0) 호출 후 (경로 압축):

0 → 1 → 2 → 3 → 4              4
                              / | \ \
                             0  1  2 3
```

다음번 `find(0)`은 단 한 번의 점프로 끝납니다. `union()`이 반복될 때마다 트리가 계속 납작해지므로, 전체적으로 `find` 연산 하나당 상수 시간에 가까워집니다.

## 4. 최적화 2: Union by Size (코드 주석은 "rank"라고 부르지만 실제로는 크기입니다)

`union()`에서 무작정 한쪽 루트를 다른 쪽 밑에 붙이면, 운이 나쁘면 다시 트리가 한쪽으로 길게 늘어질 수 있습니다. 그래서 **항상 더 작은 집합을 더 큰 집합 밑에 붙입니다.**

이 코드는 `parent[root]`가 양수가 아닐 때(즉 루트일 때) 그 값을 **"자기 집합 크기의 음수"** 로 재활용하는 트릭을 씁니다.

```
parent[i] < 0  →  i는 루트이고, 그 집합의 크기는 -parent[i]
parent[i] >= 0 →  i는 루트가 아니고, parent[i]는 i의 부모 인덱스
```

```python
def union(self, a: int, b: int):
    root_a = self.find(a)
    root_b = self.find(b)

    if root_a == root_b:
        return

    # Union by rank (size)
    if self.rank(root_a) < self.rank(root_b):
        root_a, root_b = root_b, root_a

    self.parent[root_a] += self.parent[root_b]   # 두 음수를 더해 크기를 합산
    self.parent[root_b] = root_a                 # 작은 쪽 루트를 큰 쪽 밑에 매단다
```
(`union_find.py:6-18`)

> **주의**: 코드 주석은 `# Union by rank (size)`라고 되어 있지만, 실제로 저장/비교되는 값은 트리의 "높이(rank)"가 아니라 **집합의 원소 개수(size)** 입니다. `rank(a)`(`union_find.py:26-28`)도 `-self.parent[find(a)]`, 즉 크기를 반환합니다. 고전적인 "union by rank"(트리 높이 기준)와 헷갈리기 쉬우니 주의하세요 — 이 구현은 **union by size**입니다.

```
union(0, 1) 전:  parent = [-1, -1, ...]   (0의 크기 1, 1의 크기 1)

rank(0) < rank(1)? 1 < 1 → False, 그대로 0을 큰 쪽으로 취급

parent[0] += parent[1]  →  parent[0] = -1 + -1 = -2   (집합 크기 2)
parent[1] = 0                                          (1은 0 밑으로)

union(0, 1) 후:      0 (size=2)
                      |
                      1
```

## 5. `find()`의 재귀 vs 반복 — 임계값(threshold)은 정확히 1000

이 코드는 `find()`를 **재귀 버전과 반복 버전 두 가지**로 모두 구현해두고, 구조체의 크기에 따라 자동으로 골라 씁니다.

```python
def find(self, a: int):
    if len(self.parent) > 1000:
        return self._find_by_loop(a)

    return self._find_by_recursive(a)
```
(`union_find.py:20-24`)

- **`len(self.parent) <= 1000`(1000 포함)** → `_find_by_recursive()`(재귀, `union_find.py:33-39`) 사용
- **`len(self.parent) > 1000`(1001 이상)** → `_find_by_loop()`(반복, `union_find.py:41-53`) 사용

즉 원소가 정확히 1000개일 때는 여전히 재귀 버전을 쓰고, 1001개부터 반복 버전으로 전환됩니다. (`tests/union_find/test_union_find.py`의 `TestUnionFindInstanceDispatchThreshold`가 이 경계값을 정확히 검증합니다.)

**왜 하필 1000일까?** Python의 기본 재귀 깊이 제한(`sys.getrecursionlimit()`)이 기본값 `1000`이기 때문입니다. 경로 압축이 아직 한 번도 일어나지 않은 최악의 경우, `find()`는 트리의 깊이만큼 재귀 호출을 쌓아야 할 수 있는데, 원소가 1000개를 넘어가면 이 재귀가 Python의 호출 스택 한도를 넘어 `RecursionError`를 일으킬 위험이 생깁니다. 그래서 이 코드는 **"현재 트리가 실제로 얼마나 깊은가"가 아니라 "구조체 전체 크기가 몇 개인가"** 를 기준으로 보수적으로 안전한 반복 버전으로 전환합니다.

```python
def _find_by_recursive(self, a: int):
    if self.is_root(a):
        return a

    # Path compression
    self.parent[a] = self._find_by_recursive(self.parent[a])
    return self.parent[a]
```
(`union_find.py:33-39`) — 재귀로 루트까지 내려갔다가, 되돌아오면서 지나온 모든 노드를 루트에 바로 연결합니다(경로 압축).

```python
def _find_by_loop(self, a: int):
    root = a
    while not self.is_root(root):
        root = self.parent[root]

    # Path compression
    index = a
    while index != root:
        next_index = self.parent[index]
        self.parent[index] = root
        index = next_index

    return root
```
(`union_find.py:41-53`) — 결과는 재귀 버전과 동일하지만, 두 번의 `while` 루프(① 루트 찾기, ② 경로 압축)로 재귀 호출 없이 처리합니다. 스택 깊이 걱정 없이 원소 수백만 개도 안전하게 처리할 수 있습니다.

## 6. classmethod로 제공되는 정적(static) API

`UnionFind`는 인스턴스를 만들지 않고도 **순수 함수 형태**로 똑같은 알고리즘을 쓸 수 있도록, 동일한 로직을 `@classmethod`로도 제공합니다. 인스턴스 대신 직접 만든 `parent: list[int]` 배열을 인자로 넘겨서 사용합니다.

```python
from algorithm.union_find.union_find import UnionFind

parent = [-1] * 5                     # 크기 5, 모두 자기 자신이 루트
UnionFind.union_static(parent, 0, 1)
UnionFind.union_static(parent, 1, 2)

UnionFind.find_static(parent, 0) == UnionFind.find_static(parent, 2)  # True
```

| classmethod | 대응하는 인스턴스 메서드 | 코드 위치 |
|---|---|---|
| `union_static(parent, a, b)` | `union(a, b)` | `union_find.py:55-68` |
| `find_static(parent, a)` | `find(a)` (재귀/반복 자동 분기, 임계값 동일하게 1000) | `union_find.py:70-75` |
| `find_by_recursive(parent, a)` | `_find_by_recursive(a)` | `union_find.py:77-84` |
| `find_by_loop(parent, a)` | `_find_by_loop(a)` | `union_find.py:86-99` |

`find_by_recursive`/`find_by_loop`는 `find_static`을 거치지 않고 **직접 호출해서 특정 구현을 강제**할 수도 있습니다 (테스트 코드의 `TestStaticFindImplementations`가 이렇게 사용합니다). 이 API는 여러 개의 독립적인 Union-Find 배열을 동시에 다루거나, 클래스 인스턴스 생성 오버헤드 없이 가볍게 쓰고 싶을 때 유용합니다.

## 7. 시간/공간복잡도

| 연산 | 복잡도 (경로 압축 + union by size 적용) |
|---|---|
| `find` | `O(α(n))` — 상수에 매우 가까움 |
| `union` | `O(α(n))` |
| 공간 | `O(n)` |

`α(n)`은 역 아커만 함수(inverse Ackermann function)로, 현실적인 모든 `n`에 대해 4 이하이므로 실질적으로 `O(1)`이라고 봐도 무방합니다.

## 8. 개념 ↔ 코드 대응표

| 개념 | 코드 위치 |
|---|---|
| 부모/크기 인코딩 배열 (`parent[i] < 0`이면 루트, 값은 `-크기`) | `self.parent` (`union_find.py:4`) |
| 루트 여부 판별 | `is_root()` (`union_find.py:30-31`) |
| 두 집합 합치기 (union by size) | `union()` (`union_find.py:6-18`) |
| 집합 크기 조회 | `rank()` (`union_find.py:26-28`) |
| 재귀/반복 자동 분기 (임계값 1000) | `find()` (`union_find.py:20-24`) |
| 재귀 방식 경로 압축 | `_find_by_recursive()` (`union_find.py:33-39`) |
| 반복 방식 경로 압축 | `_find_by_loop()` (`union_find.py:41-53`) |
| 정적(classmethod) 유틸리티 — 합치기 | `union_static()` (`union_find.py:55-68`) |
| 정적 유틸리티 — 탐색 자동 분기 | `find_static()` (`union_find.py:70-75`) |
| 정적 유틸리티 — 재귀 탐색 | `find_by_recursive()` (`union_find.py:77-84`) |
| 정적 유틸리티 — 반복 탐색 | `find_by_loop()` (`union_find.py:86-99`) |

## 9. 직접 실행해보기

`union_find.py`에는 `if __name__ == '__main__':` 데모 블록이 없습니다. 대신 pytest로 동작을 확인하거나, 아래처럼 REPL에서 직접 실습해볼 수 있습니다.

```bash
python3 -m pytest tests/union_find/test_union_find.py -v
```

```python
from algorithm.union_find.union_find import UnionFind

uf = UnionFind(6)
uf.union(0, 1)
uf.union(1, 2)
uf.union(3, 4)

print(uf.find(0) == uf.find(2))   # True  (0-1-2는 같은 집합)
print(uf.find(0) == uf.find(3))   # False (다른 집합)
print(uf.rank(uf.find(0)))        # 3     (집합 크기)
```

`tests/union_find/test_union_find.py`의 `TestUnionFindInstanceDispatchThreshold` / `TestUnionFindStaticDispatchThreshold` 클래스를 읽어보면, 정확히 1000개를 기준으로 재귀/반복이 갈리는 것을 `monkeypatch`로 어떻게 검증하는지도 확인할 수 있습니다.

---

이전 문서: 없음 (그래프 알고리즘 문서 시리즈 시작)
다음 문서: [최소 신장 트리 (MST) →](../mst/README.md)
