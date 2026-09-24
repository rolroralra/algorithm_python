# 최소 공통 조상 (Lowest Common Ancestor, LCA)

> 구현: [`lca.py`](./lca.py) — `LCA` 클래스

## 1. 왜 LCA가 필요한가?

트리(회사 조직도, 파일 시스템, 생물 분류 체계, 게임 스킬 트리 등)에서 서로 다른 두 노드를 보고 이런 질문을 던질 때가 많습니다.

- "이 두 직원의 공통 상사 중 가장 가까운 사람은 누구인가?" (조직도)
- "이 두 파일이 공유하는 가장 안쪽 디렉토리는 어디인가?" (파일 시스템)
- "트리에서 두 노드 사이의 최단 경로 길이는?" → `depth[a] + depth[b] - 2 * depth[lca(a,b)]`로 바로 계산 가능

이렇게 "두 노드에서 각자 루트 방향으로 올라갈 때 처음 만나는 공통 조상"을 **최소 공통 조상(LCA)** 이라고 부릅니다.

```
              0
             / \
            1   2
           / \   \
          3   4   5

lca(3, 4) = 1   (형제 노드 → 부모가 LCA)
lca(3, 5) = 0   (서로 다른 서브트리 → 루트가 LCA)
lca(3, 1) = 1   (한쪽이 다른 쪽의 조상이면, 그 조상 자신이 LCA)
```

가장 단순한 방법은 "두 노드에서 부모를 한 칸씩 번갈아 타고 올라가며 처음 만나는 지점을 찾는" **부모 포인터 순회(parent-pointer walk)** 입니다. 이 방법은 쿼리 하나당 `O(depth)`가 걸리는데, 트리가 한쪽으로 치우쳐 있으면(연결 리스트에 가까우면) 최악의 경우 `O(n)`까지 느려질 수 있습니다.

## 2. 이 코드의 구현 방식: 이진 리프팅 (Binary Lifting / Sparse Table)

`lca.py`는 부모 포인터를 한 칸씩 순회하는 대신, **"2의 거듭제곱 칸만큼 한 번에 점프"** 할 수 있는 조상 테이블(sparse table)을 미리 만들어둡니다. 이 기법을 **이진 리프팅(binary lifting)** 이라고 부릅니다.

```
parent[node][k] = node의 2^k번째 조상

parent[node][0] = 바로 위 부모 (2^0 = 1칸)
parent[node][1] = 2칸 위 조상 (2^1 = 2칸)
parent[node][2] = 4칸 위 조상 (2^2 = 4칸)
...
```

임의의 거리만큼 올라가는 것도, 그 거리를 이진수로 쪼개서 몇 번의 점프로 표현할 수 있습니다. 예를 들어 5칸 위로 가고 싶다면 `5 = 4 + 1`이므로 "4칸 점프 한 번 + 1칸 점프 한 번" 딱 2번으로 끝납니다. 그래서 쿼리 하나가 `O(log n)`에 끝납니다.

## 3. `__init__` / `build()` — 조상 테이블 만들기

```python
def __init__(self, size):
    self.size = size
    self.LOGN = (size - 1).bit_length()                          # 필요한 최대 2^k 지수
    self.parent = [[-1] * (self.LOGN + 1) for _ in range(size)]   # 조상 테이블
    self.depth = [-1] * size
```
(`lca.py:1-8`)

`LOGN`은 `size`개의 노드를 커버하는 데 필요한 최대 지수입니다(예: 노드 10개면 `(10-1).bit_length() = 4`, 즉 `2^4=16`칸까지 표현 가능).

```python
def build(self, adj_list, root_index=0):
    stack = []
    depth[root_index] = 0
    stack.append(root_index)
    while stack:
        curr_index = stack.pop()
        for next_index in adj_list[curr_index]:
            if depth[next_index] != -1:
                continue

            parent[next_index][0] = curr_index                    # 2^0 조상 = 바로 위 부모
            for depth_level in range(1, LOGN + 1):
                if parent[next_index][depth_level - 1] != -1:
                    parent[next_index][depth_level] = parent[parent[next_index][depth_level - 1]][depth_level - 1]
                    # "2^k 조상 = (2^(k-1) 조상)의 2^(k-1) 조상"

            depth[next_index] = depth[curr_index] + 1
            stack.append(next_index)
```
(`lca.py:11-33`)

스택을 이용한 DFS로 트리를 순회하면서, 각 노드를 처음 방문하는 그 순간에 바로 조상 테이블 한 줄을 완성합니다. 핵심 점화식은 `parent[node][k] = parent[parent[node][k-1]][k-1]` — "2^k칸 위로 가려면, 먼저 2^(k-1)칸 올라간 다음 거기서 다시 2^(k-1)칸 올라가면 된다"는 분할 정복 아이디어입니다.

```
2^0 조상(부모)만 안다면:          이걸로 2^1, 2^2, ... 조상을 연쇄적으로 계산:

  D → C → B → A (루트)          parent[D][1] = parent[ parent[D][0] ][0] = parent[C][0] = B
                                  parent[D][2] = parent[ parent[D][1] ][1] = parent[B][1] = A (B의 2칸 위)
```

## 4. `lca(a, b)` — 두 단계로 답을 찾는다

```python
def lca(self, a, b):
    if depth[a] < depth[b]:
        a, b = b, a                                    # a가 항상 더 깊거나 같도록 맞춤

    # 1단계: a를 b와 같은 깊이까지 끌어올린다
    for depth_level in range(LOGN, -1, -1):
        if depth[a] - depth[b] >= (1 << depth_level):
            a = parent[a][depth_level]

    if a == b:
        return a                                        # b가 a의 조상이었던 경우 → 그 자체가 LCA

    # 2단계: a, b를 동시에, 서로 달라지는 한도까지 최대한 높이 점프
    for depth_level in range(LOGN, -1, -1):
        if parent[a][depth_level] != -1 and parent[a][depth_level] != parent[b][depth_level]:
            a = parent[a][depth_level]
            b = parent[b][depth_level]

    return parent[a][0]                                   # 한 칸만 더 올라가면 LCA
```
(`lca.py:36-57`)

```
예시: lca(3, 5)   (트리는 1장의 그림과 동일, depth[3]=2, depth[5]=2)

1단계: depth[3]==depth[5] 이므로 끌어올릴 필요 없음
2단계: parent[3][0]=1, parent[5][0]=2  → 서로 다름 → 동시에 1칸 점프
       a=1, b=2

a==b? 1==2 → False, 루프는 이미 depth_level=0까지 다 봤으므로 종료
return parent[a][0] = parent[1][0] = 0   ← 0이 정답!
```

큰 지수(`depth_level`이 큰 쪽)부터 시도하면서, "점프해도 여전히 서로 다른 노드"일 때만 실제로 점프합니다. 이렇게 하면 `a`와 `b`가 **LCA 바로 아래 자식들**에서 멈추게 되고, 마지막에 부모를 한 번 더 타면 정확히 LCA에 도착합니다.

## 5. 시간/공간복잡도

| 연산 | 부모 포인터 순회 (naive) | 이진 리프팅 (이 코드) |
|---|---|---|
| 전처리(build) | `O(n)` | `O(n log n)` |
| 쿼리(lca) 1회 | `O(depth)`, 최악 `O(n)` | `O(log n)` |
| 공간 | `O(n)` | `O(n log n)` (조상 테이블) |

트리 깊이가 깊어질 위험이 있거나(편향된 트리) LCA 쿼리가 여러 번 반복될 때, 전처리 비용을 조금 더 들이더라도 쿼리당 `O(log n)`을 보장하는 이진 리프팅이 유리합니다.

## 6. 개념 ↔ 코드 대응표

| 개념 | 코드 위치 |
|---|---|
| LCA 클래스 | `LCA` (`lca.py:1`) |
| 조상 테이블 크기 계산 | `self.LOGN = (size - 1).bit_length()` (`lca.py:6`) |
| 2^k 조상 테이블 | `self.parent` (`lca.py:7`) |
| 각 노드의 깊이 | `self.depth` (`lca.py:8`) |
| 트리 순회 + 조상 테이블 구축 | `build()` (`lca.py:11-33`) |
| 이진 리프팅 점화식 | `parent[next_index][depth_level] = parent[parent[next_index][depth_level-1]][depth_level-1]` (`lca.py:30`) |
| 깊이 맞추기 (1단계) | `lca()` 앞부분 (`lca.py:42-47`) |
| 동시 점프로 LCA 바로 아래까지 접근 (2단계) | `lca()` 뒷부분 (`lca.py:52-55`) |
| 깊이 조회 | `get_depth()` (`lca.py:60-61`) |

## 7. 직접 실행해보기

`lca.py`에는 `if __name__ == '__main__':` 데모 블록이 없습니다. pytest로 동작을 확인하거나, 아래처럼 직접 실습해볼 수 있습니다.

```bash
python3 -m pytest tests/lca/test_lca.py -v
```

```python
from algorithm.lca.lca import LCA

# tree:            0
#                 / \
#                1   2
#               / \   \
#              3   4   5
adj = [[1, 2], [0, 3, 4], [0, 5], [1], [1], [2]]
lca = LCA(6)
lca.build(adj, root_index=0)

print(lca.lca(3, 4))   # 1
print(lca.lca(3, 5))   # 0
print(lca.get_depth(4))  # 2
```

---

이전 문서: [← 최소 신장 트리 (MST)](../mst/README.md)
다음 문서: [단절점과 단절선 (Articulation Points & Bridges) →](../articulation/README.md)
