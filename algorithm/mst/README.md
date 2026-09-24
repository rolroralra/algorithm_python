# 최소 신장 트리 (Minimal Spanning Tree, MST)

> 구현: [`minimal_spanning_tree.py`](./minimal_spanning_tree.py) — `mst_kruskal_algorithm()`, `mst_prim_algorithm()`, 그리고 이 둘을 감싸는 `minimal_spanning_tree()` 디스패처
> 이 문서를 읽기 전에 [union_find/README.md](../union_find/README.md)를 먼저 읽는 것을 권장합니다. Kruskal 알고리즘에서 바로 사용됩니다.

## 1. 왜 MST가 필요한가?

여러 도시를 통신망(또는 도로, 전선)으로 모두 연결해야 하는데, 도시마다 연결 비용이 다르다고 해봅시다. 목표는:

- 모든 도시가 (직접이든 간접이든) 서로 연결되어야 하고
- 연결에 드는 총 비용은 최소여야 한다

이 문제를 그래프로 옮기면: 정점(도시) `V`개를 모두 연결하는 부분 그래프 중, **사이클이 없고**(트리), **간선 가중치의 합이 최소**인 트리를 찾는 문제가 됩니다. 이것이 **최소 신장 트리(MST)** 입니다.

```
전체 그래프 (간선이 많고 비용도 다양함):        선택된 MST (정점 4개 → 간선 정확히 3개):

    0 --4-- 1                                    0       1
    |\      |\                                    \       \
    1| \2    5|                                     1       2
    | 3\    | \                                      \       \
    2 --8-- 3--4                                        2       3
```

정점이 `V`개인 신장 트리(spanning tree)는 항상 정확히 `V - 1`개의 간선을 가집니다. 간선이 그보다 많으면 반드시 사이클이 생기고, 적으면 모든 정점이 연결될 수 없습니다.

## 2. 이 코드에 구현된 두 알고리즘

`minimal_spanning_tree.py`에는 MST를 구하는 두 가지 고전 알고리즘이 모두 구현되어 있고, `MinimalSpanningTreeAlgorithm` Enum과 `minimal_spanning_tree()` 함수로 어느 쪽을 쓸지 선택할 수 있습니다 (`minimal_spanning_tree.py:5-15`).

```python
class MinimalSpanningTreeAlgorithm(Enum):
    KRUSKAL_ALGORITHM = 1
    PRIM_ALGORITHM = 2

def minimal_spanning_tree(graph, algorithm: MinimalSpanningTreeAlgorithm):
    if algorithm == MinimalSpanningTreeAlgorithm.KRUSKAL_ALGORITHM:
        return mst_kruskal_algorithm(graph)
    elif algorithm == MinimalSpanningTreeAlgorithm.PRIM_ALGORITHM:
        return mst_prim_algorithm(graph)
```

둘 다 **그리디(greedy) 알고리즘**입니다 — 매 순간 "지금 볼 수 있는 선택지 중 가장 싼 것"을 고르는데, 놀랍게도 이 지역적(local) 선택만으로 전역(global) 최적해인 MST가 만들어진다는 것이 증명되어 있습니다(Cut Property). 단, 두 알고리즘은 "무엇을 기준으로 그리디하게 고르는가"가 다릅니다.

## 3. Kruskal 알고리즘 — "가장 싼 간선"부터 그리디하게

**아이디어**: 모든 간선을 가중치 오름차순으로 정렬한 뒤, 싼 것부터 하나씩 보면서 **사이클을 만들지 않는 간선만** 채택합니다. 간선을 `V - 1`개 모으면(=신장 트리가 완성되면) 종료합니다.

```python
def mst_kruskal_algorithm(edge_list, vertex_size=None):
    edge_list.sort(key=lambda edge: edge[2])          # 가중치 오름차순 정렬 (minimal_spanning_tree.py:28)
    ...
    union_find = UnionFind(vertex_size)                # minimal_spanning_tree.py:37

    for a, b, length in edge_list:                     # minimal_spanning_tree.py:43
        if union_find.find(a) != union_find.find(b):    # 사이클 판별 (minimal_spanning_tree.py:44)
            union_find.union(a, b)                      # 채택 → 두 집합을 합친다 (minimal_spanning_tree.py:45)
            selected_edge_list.append((a, b, length))
            edge_selected_count += 1
            mst_length += length

        if edge_selected_count == vertex_size - 1:       # V-1개 모이면 조기 종료 (minimal_spanning_tree.py:50-51)
            break
```
(`minimal_spanning_tree.py:18-53`)

### 왜 사이클 판별이 필요한가?

간선 `(a, b)`를 추가하려는데 `a`와 `b`가 **이미 같은 집합**(즉 이미 연결되어 있는 상태)이라면, 이 간선을 추가하는 순간 둘 사이에 두 번째 경로가 생겨 **사이클**이 만들어집니다. 트리는 정의상 사이클이 없어야 하므로, 그런 간선은 버려야 합니다.

```
이미 연결됨: 0 --1-- 1 --2-- 2       간선 (0,2, 길이=3) 후보

find(0) == find(2) ? → 이미 같은 집합(트리) → 추가하면 사이클! → 버림

    0---1---2
     \_____/   ← 이 간선을 추가하면 삼각형(사이클)이 생김
```

바로 이 판별을 [union_find/README.md](../union_find/README.md)에서 설명한 `union_find.find(a) != union_find.find(b)`(`minimal_spanning_tree.py:44`)가 담당합니다. `find` 결과가 다르면 아직 연결되지 않은 서로 다른 두 컴포넌트이므로, 안전하게 이어 붙이고(`union`) MST에 채택합니다.

### 왜 그리디가 통하는가?

"가장 싼 간선부터 사이클만 피해서 담는다"는 지역적 선택이 전역 최적이 되는 이유는 **Cut Property**(절단 성질) 때문입니다: 그래프를 두 그룹으로 나누는 어떤 절단(cut)을 생각했을 때, 그 절단을 가로지르는 간선 중 가장 싼 것은 반드시 어떤 MST에도 포함됩니다. Kruskal은 정렬 순서대로 간선을 보면서 매번 이 성질을 만족시키기 때문에 최적해가 보장됩니다.

## 4. Prim 알고리즘 — "지금까지 만든 트리에 가장 싸게 붙는 정점"부터 그리디하게

**아이디어**: 정점 하나(`0`번)에서 시작해서, 지금까지 만든 트리에 인접한 간선 중 **가장 싼 것**을 하나씩 붙여 나갑니다. 우선순위 큐(최소 힙)로 "다음으로 가장 싸게 붙일 수 있는 간선"을 항상 `O(log V)`에 꺼냅니다.

```python
def mst_prim_algorithm(adj_list):
    is_visited = [False] * vertex_count
    priority_queue = PriorityQueue()

    priority_queue.put((0, 0, -1))                     # (간선 길이, 시작 정점=0, 이전 정점=-1: 자기 자신이라 무시)
    while not priority_queue.empty():
        curr_edge_length, curr_index, prev_index = priority_queue.get()   # 가장 싼 간선부터 pop

        if is_visited[curr_index]:
            continue                                    # 이미 트리에 포함된 정점 → 지연 삭제(lazy deletion)

        is_visited[curr_index] = True
        if prev_index != -1:
            mst_length += curr_edge_length
            selected_edge_list.append((prev_index, curr_index, curr_edge_length))

        if len(selected_edge_list) == vertex_count - 1:
            break

        for next_index, next_edge_length in adj_list[curr_index]:
            if is_visited[next_index]:
                continue
            priority_queue.put((next_edge_length, next_index, curr_index))
```
(`minimal_spanning_tree.py:56-93`)

```
시작: 0번 정점만 트리에 포함, (0, 0, -1)을 큐에 미리 넣어둔다 (스스로에게 오는 가짜 간선, 길이 0)

  트리 = {0}          큐 = [(0, 0, -1)]

pop (0, 0, -1) → 0을 방문 처리, prev=-1이라 트리 길이에는 더하지 않음
                 → 0의 인접 간선을 모두 큐에 push

  트리 = {0}          큐 = [(1,1,0), (3,2,0), ...]   (가중치 순으로 자동 정렬)

pop 가장 싼 것 (1,1,0) → 1을 방문, 트리에 간선 (0,1,길이1) 추가
                       → 1의 인접 간선들도 큐에 push (이미 방문한 0은 스킵)
     ... 반복 ...
```

`is_visited[curr_index]`가 `True`인 항목을 만나면 그냥 건너뛰는 방식(**지연 삭제, lazy deletion**)을 쓰기 때문에, 큐에는 같은 정점을 가리키는 오래된(더 비싼) 항목이 남아있어도 상관없습니다 — 어차피 먼저 꺼내지는 더 싼 항목이 처리되고 나면 그 뒤에 꺼내지는 것들은 전부 무시됩니다. Dijkstra 알고리즘과 매우 비슷한 구조입니다 (차이점: 누적 거리 대신 "간선 하나의 길이"만 비교).

## 5. Kruskal vs Prim 비교

| | Kruskal | Prim (이 코드의 구현) |
|---|---|---|
| 그리디 기준 | 전체 간선 중 가장 싼 것 | 현재 트리에 인접한 가장 싼 것 |
| 사용 자료구조 | Union-Find (사이클 판별) | Priority Queue (최소 힙) |
| 입력 형태 | 간선 리스트 `(a, b, length)` | 인접 리스트 `[[(다음 정점, 길이), ...], ...]` |
| 시간복잡도 | `O(E log E)` (정렬이 지배적) | `O(E log V)` (힙에 각 간선을 최대 1번 push) |
| 유리한 상황 | 간선이 상대적으로 적은 **희소 그래프** | 간선이 많은 **조밀 그래프** |

두 알고리즘 모두 같은 그래프에 대해 항상 같은 MST 총 길이를 반환합니다(선택되는 구체적인 간선 집합은 가중치가 같은 간선이 여러 개 있을 경우 다를 수 있습니다). `tests/mst/test_minimal_spanning_tree.py`의 `test_matches_kruskal_on_same_graph`가 이를 직접 검증합니다.

## 6. 몇 가지 구현 디테일

- **`vertex_size` 자동 추론**: Kruskal 호출 시 `vertex_size`를 생략하면, 간선 리스트에 등장하는 모든 정점 번호를 모아 `set`으로 개수를 센 뒤 사용합니다(`minimal_spanning_tree.py:30-35`).
- **조기 종료**: 두 알고리즘 모두 선택된 간선이 `V - 1`개가 되는 순간 나머지 간선/큐 항목을 더 볼 필요 없이 바로 반복문을 빠져나옵니다(`minimal_spanning_tree.py:50-51`, `84-85`).
- **Prim의 시작 정점**: 코드는 항상 `0`번 정점에서 시작합니다(`priority_queue.put((0, 0, -1))`, `minimal_spanning_tree.py:72`). 그래프가 연결되어 있다면 시작 정점이 어디든 결과 MST 길이는 동일합니다.

## 7. 시간/공간복잡도

| 알고리즘 | 시간복잡도 | 공간복잡도 |
|---|---|---|
| Kruskal (`mst_kruskal_algorithm`) | `O(E log E)` | `O(V + E)` |
| Prim (`mst_prim_algorithm`) | `O(E log V)` | `O(V + E)` |

## 8. 개념 ↔ 코드 대응표

| 개념 | 코드 위치 |
|---|---|
| 알고리즘 선택 Enum | `MinimalSpanningTreeAlgorithm` (`minimal_spanning_tree.py:5-7`) |
| 알고리즘 디스패처 | `minimal_spanning_tree()` (`minimal_spanning_tree.py:9-15`) |
| Kruskal 알고리즘 | `mst_kruskal_algorithm()` (`minimal_spanning_tree.py:18-53`) |
| 간선 정렬 (그리디의 핵심) | `edge_list.sort(...)` (`minimal_spanning_tree.py:28`) |
| 사이클 판별 (Union-Find 활용) | `union_find.find(a) != union_find.find(b)` (`minimal_spanning_tree.py:44`) |
| Prim 알고리즘 | `mst_prim_algorithm()` (`minimal_spanning_tree.py:56-93`) |
| 최소 힙으로 "가장 싼 간선" 관리 | `PriorityQueue` (`minimal_spanning_tree.py:67, 72, 91`) |
| 지연 삭제(lazy deletion) | `if is_visited[curr_index]: continue` (`minimal_spanning_tree.py:76-77`) |

## 9. 직접 실행해보기

`minimal_spanning_tree.py`에는 `if __name__ == '__main__':` 데모 블록이 없습니다. pytest로 동작을 확인하거나, 아래처럼 직접 실습해볼 수 있습니다.

```bash
python3 -m pytest tests/mst/test_minimal_spanning_tree.py -v
```

```python
from algorithm.mst.minimal_spanning_tree import mst_kruskal_algorithm, mst_prim_algorithm

edges = [(0, 1, 4), (0, 2, 1), (1, 2, 2), (1, 3, 5), (2, 3, 8), (2, 4, 10), (3, 4, 2)]
adj_list = [[] for _ in range(5)]
for a, b, length in edges:
    adj_list[a].append((b, length))
    adj_list[b].append((a, length))

print(mst_kruskal_algorithm(list(edges), vertex_size=5))   # (length, selected_edges)
print(mst_prim_algorithm(adj_list))                          # 같은 length, 다를 수 있는 selected_edges
```

---

이전 문서: [← Union-Find (Disjoint Set Union)](../union_find/README.md)
다음 문서: [최소 공통 조상 (LCA) →](../lca/README.md)
