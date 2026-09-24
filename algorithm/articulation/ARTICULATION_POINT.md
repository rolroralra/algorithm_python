# 단절점 (Articulation Point / Cut Vertex)

> 구현: [`articulation_point.py`](./articulation_point.py) — `articulation_points()`
> 이 문서를 읽기 전에 [README.md](./README.md)의 "단절점 vs 단절선" 구분과 discovery time / low-link 개념을 먼저 읽어주세요.

## 1. DFS Spanning Tree와 두 종류의 간선

그래프를 DFS로 순회하면, 실제로 타고 내려간 간선들이 하나의 **DFS 신장 트리(spanning tree)** 를 이룹니다. 이때 나머지 간선은 전부 **역방향 간선(back edge)** — 이미 방문한 조상 쪽으로 되돌아가는 간선입니다(이 코드가 다루는 무방향 그래프에서는 "전진 간선/교차 간선"이 생기지 않습니다).

```
그래프:                          DFS(0에서 시작) 결과 — 트리 간선(─)과 역방향 간선(╌):

    0---1---3---4                       0
     \ /                                │(트리)
      2                                 1───────╮
                                       ╱ │       │(트리)
                                  (트리)│      3
                                     2   ╲(트리)  │(트리)
                                      ╲___╌╌╌╌   4
                                     (역방향 간선: 2→0)
```

## 2. discovery time과 low-link 값

`articulation_point.py`는 정점을 방문한 순서를 `visit[]`(discovery time)에 기록하고, DFS가 각 노드에서 돌아올 때 `min_visit_sequence`(low-link 값)를 계산해서 반환합니다.

```python
def dfs(curr_index: int, is_root: bool = False) -> int:
    if visit[curr_index] > 0:
        return visit[curr_index]

    visit[curr_index] = visit_sequence      # discovery time 기록
    visit_sequence += 1

    min_visit_sequence = visit[curr_index]  # low-link 초깃값 = 자기 자신의 discovery time
    child_count = 0

    for next_index in adj_list[curr_index]:
        if visit[next_index] == 0:
            child_count += 1
            min_visit_seq_from_child = dfs(next_index)          # 자식으로 재귀 → 자식의 low-link를 받음

            if not is_root and min_visit_seq_from_child >= visit[curr_index]:
                is_articulation_point[curr_index] = True         # 핵심 판정!
        else:
            min_visit_seq_from_child = visit[next_index]          # 역방향 간선 → 상대의 discovery time

        min_visit_sequence = min(min_visit_sequence, min_visit_seq_from_child)

    if is_root and child_count >= 2:
        is_articulation_point[curr_index] = True                  # 루트 전용 특수 케이스

    return min_visit_sequence
```
(`articulation_point.py:7-45`)

`visit[curr_index] > 0`(21-22번째 줄)은 이미 방문한 노드에 `dfs()`가 다시 호출됐을 때의 안전장치입니다. 실제로 이 코드에서 `dfs()`는 항상 `visit[next_index] == 0`(미방문)을 먼저 확인한 뒤에만 재귀 호출되므로(30-31번째 줄), 이 가드는 현재 호출 경로에서는 실질적으로 발동하지 않는 방어 코드입니다.

## 3. 핵심 판정 조건: `low[child] >= discovery[curr]` (루트가 아닐 때)

어떤 정점 `curr`의 자식 `child`에 대해, `child`의 서브트리가 **역방향 간선을 통해서도 `curr`보다 더 위쪽 조상으로 올라가지 못한다면**(즉 `low[child] >= discovery[curr]`), `curr`을 제거하는 순간 `child`의 서브트리는 나머지 그래프와 완전히 단절됩니다. 그래서 `curr`은 단절점입니다.

```
예시 그래프(README의 공통 예시)에서 DFS(0 → 1 → 2, 0 → 1 → 3 → 4 순서로 진행):

  discovery(visit): 0→1, 1→2, 2→3, 3→4, 4→5
  low-link:          low[4]=4, low[3]=2, low[2]=1, low[1]=1, low[0]=1

  low[4] >= visit[3] ?   4 >= 4  → True  → 3은 단절점!  (4는 3을 거치지 않고는 못 나감)
  low[3] >= visit[1] ?   2 >= 2  → True  → 1은 단절점!  (3,4의 서브트리는 1을 거치지 않고는 못 나감)
  low[2] >= visit[0] ?   1 >= 1  → 하지만 0은 루트라서 이 조건 자체를 적용하지 않음 (아래 4장 참고)

결과: articulation_points(adj_list) == [1, 3]   ✅ 테스트 결과와 일치
```

## 4. 루트 노드의 특수 케이스: 왜 "자식이 2개 이상이면 단절점"인가?

DFS 루트(`is_root=True`)는 부모가 없기 때문에, "역방향 간선으로 조상에 닿을 수 있는가"라는 `low >= discovery` 비교 자체가 성립하지 않습니다(비교할 조상이 없으므로). 그래서 루트는 완전히 다른 기준으로 판정합니다.

```python
if is_root and child_count >= 2:
    is_articulation_point[curr_index] = True
```
(`articulation_point.py:42-43`)

**왜 자식이 2개 이상이면 루트가 단절점일까?** DFS 트리에서 루트의 서로 다른 자식들이 이끄는 서브트리들은, **루트를 거치지 않고는 서로 연결될 방법이 없습니다.** (만약 두 서브트리 사이에 역방향 간선이 있었다면, DFS가 애초에 그 간선을 타고 하나의 서브트리로 합쳐 탐색했을 것이기 때문입니다.) 따라서 루트에 자식이 2개 이상이면, 루트를 지우는 순간 그 서브트리들이 서로 분리됩니다.

```
루트(0)의 자식이 2개(1, 2)이고 서로 역방향 간선으로 이어져 있지 않다면:

        0                       0 제거 →      1       2
       / \                                  (연결 끊김)
      1   2

반대로 자식이 1개뿐이면(전형적인 예: README의 공통 예시에서 0의 자식은 1 하나뿐):

        0                       0 제거 →      1
        |                                    / \
        1                                   2   3
       / \                                       \
      2   3                                        4
           \
            4
→ 0은 단절점이 아님 (child_count == 1이라 조건 불만족, 실제로도 1-2-3-4가 모두 그대로 연결됨)
```

## 5. 시간/공간복잡도

| 항목 | 복잡도 |
|---|---|
| 시간 | `O(V + E)` — 모든 정점과 간선을 한 번씩만 방문 |
| 공간 | `O(V)` — `visit`, `is_articulation_point` 배열 + 재귀 스택 |

## 6. 개념 ↔ 코드 대응표

| 개념 | 코드 위치 |
|---|---|
| 진입점 (모든 연결 요소를 순회) | `for i in range(vertex_count): if visit[i] == 0: dfs(i, True)` (`articulation_point.py:47-49`) |
| discovery time (방문 순서) | `visit[]` (`articulation_point.py:4`) |
| low-link 값 계산 및 반환 | `dfs()`의 반환값 `min_visit_sequence` (`articulation_point.py:27, 45`) |
| 단절점 여부 저장 | `is_articulation_point[]` (`articulation_point.py:3`) |
| 비-루트 판정 조건 (`low[child] >= discovery[curr]`) | `articulation_point.py:35-36` |
| 루트 전용 판정 조건 (자식 2개 이상) | `articulation_point.py:42-43` |

## 7. 직접 실행해보기

`articulation_point.py`에는 `if __name__ == '__main__':` 데모 블록이 없습니다. pytest로 동작을 확인하거나, 아래처럼 직접 실습해볼 수 있습니다.

```bash
python3 -m pytest tests/articulation/test_articulation_point.py -v
```

```python
from algorithm.articulation.articulation_point import articulation_points

# 삼각형 0-1-2, 다리 1-3, 펜던트 3-4
adj_list = [[1, 2], [0, 2, 3], [0, 1], [1, 4], [3]]
print(articulation_points(adj_list))   # [1, 3]
```

---

이전 문서: [← 단절점과 단절선 (인덱스)](./README.md)
다음 문서: [단절선 (Articulation Edge) →](./ARTICULATION_EDGE.md)
