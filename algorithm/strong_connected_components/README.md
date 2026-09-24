# 강한 연결 요소 (Strongly Connected Components, SCC)

> 구현: [`strongly_connected_components.py`](./strongly_connected_components.py) — `scc_by_tarjan()`, `scc_by_kosaraju()`
> 관련 테스트: [`test_strongly_connected_components.py`](../../tests/strong_connected_components/test_strongly_connected_components.py)
> 이 문서를 읽기 전에 [DFS](../dfs/README.md), [위상 정렬](../topological_sort/README.md), [단절점/단절선](../articulation/README.md)(discovery time, low-link 개념)을 먼저 읽는 것을 권장합니다.

## 1. 왜 강한 연결 요소가 필요한가?

방향 그래프(directed graph)에서 두 노드 `u`, `v`가 있을 때, `u`에서 `v`로 가는 길도 있고 `v`에서 `u`로 되돌아오는 길도 있다면 이 둘은 "서로 도달 가능"합니다. 이렇게 **서로 도달 가능한 노드들을 최대한 크게 묶은 그룹**을 강한 연결 요소(SCC)라고 부릅니다.

```
0 ──► 1 ──► 2        3 ──► 4
▲     │     │        ▲     │
└─────┘     ▼        └─────┘
            (여기서 2 -> 3 간선이 있다고 하면)

SCC:  {0, 1, 2}   {3, 4}
```

`0 → 1 → 2 → 0`처럼 사이클을 이루는 노드들은 서로 왕복이 가능하므로 하나의 SCC로 묶입니다. `2 → 3`처럼 그룹 사이를 잇는 간선은 있지만 되돌아오는 길이 없으면, `2`가 속한 그룹과 `3`이 속한 그룹은 서로 다른 SCC로 남습니다.

**왜 유용한가?**
- 웹 페이지 그래프에서 "서로 링크를 주고받는 페이지 묶음"을 찾는 데 쓰입니다.
- 각 SCC를 하나의 노드로 압축(condensation)하면 원래 그래프가 항상 **DAG(방향 비순환 그래프)** 가 되므로, [위상 정렬](../topological_sort/README.md)을 적용할 수 있는 형태로 단순화할 수 있습니다.
- 2-SAT 문제(불리언 만족 문제의 한 종류)를 그래프 문제로 바꿔 풀 때 SCC가 핵심적으로 사용됩니다.
- 소프트웨어 모듈 간 의존 관계에서 "순환 의존(circular dependency)"을 찾아내는 데도 같은 원리가 쓰입니다.

이 저장소는 SCC를 구하는 대표적인 두 알고리즘, **Tarjan 알고리즘**과 **Kosaraju 알고리즘**을 모두 구현합니다.

## 2. Tarjan 알고리즘 — DFS 한 번으로 끝내기

**핵심 아이디어**: [단절점(Articulation Point)](../articulation/ARTICULATION_POINT.md)과 [단절선(Articulation Edge)](../articulation/ARTICULATION_EDGE.md)에서 사용한 **discovery time(방문 순서)** 과 **low-link(자신 또는 자손이 back edge로 거슬러 올라갈 수 있는 가장 이른 방문 순서)** 개념을 그대로 방향 그래프에 적용합니다.

차이점은, 방향 그래프에서는 단순히 "부모로 거슬러 올라가는 간선"뿐 아니라 **"현재 DFS 스택에 아직 남아있는 노드로 되돌아가는 간선"** 까지 고려해야 한다는 점입니다. 그래서 스택에 아직 남아있는지 추적하는 `on_stack` 배열이 필요합니다(`strongly_connected_components.py:6`).

```python
visit[curr_index] = low_link[curr_index] = visit_sequence   # strongly_connected_components.py:20-21
stack.append(curr_index)
on_stack[curr_index] = True                                 # strongly_connected_components.py:24

for next_index in adj_list[curr_index]:
    if visit[next_index] == 0:                               # 아직 방문 전 -> 더 깊이 탐색
        dfs(next_index)
        low_link[curr_index] = min(low_link[curr_index], low_link[next_index])
    elif on_stack[next_index]:                                # 방문했지만 "아직 스택에 남아있음" -> 같은 SCC 후보
        low_link[curr_index] = min(low_link[curr_index], visit[next_index])
```

`on_stack[next_index]` 확인이 핵심입니다. 이미 방문했더라도 스택에서 빠져나간(= 이미 다른 SCC로 확정된) 노드라면 무시해야 하고, 아직 스택에 남아있는 노드라면 "나와 같은 SCC일 가능성이 있는 조상"이므로 low-link를 갱신합니다.

### SCC 확정 시점

```
low_link[curr_index] == visit[curr_index]
```

이 조건은 "curr_index가 자기 자신보다 더 이른 조상으로 거슬러 올라갈 방법이 전혀 없다"는 뜻입니다. 즉 curr_index가 지금까지 스택에 쌓인 SCC 그룹의 **루트(가장 먼저 방문된 노드)** 라는 의미이므로, 이 시점에 스택에서 curr_index가 나올 때까지 노드를 꺼내 하나의 SCC로 묶습니다(`strongly_connected_components.py:33-40`).

```
스택(아래 -> 위):  [0, 1, 2]     curr_index = 0, low_link[0] == visit[0]
                              -> pop: 2, 1, 0 모두 하나의 SCC = {0, 1, 2}
```

## 3. Kosaraju 알고리즘 — 그래프를 뒤집어 두 번 DFS

**핵심 아이디어**: 그래프를 한 번 순회해 "언제 끝났는지(finish order)" 순서를 기록한 뒤, **모든 간선을 뒤집은 그래프**에서 끝난 순서의 역순으로 다시 DFS를 돕니다. 이때 한 번의 DFS 호출로 방문되는 노드들이 정확히 하나의 SCC를 이룹니다.

```python
# 1단계: 원래 그래프에서 DFS, 끝난 순서를 기록
def dfs_finish_order(curr_index):
    is_visited[curr_index] = True
    for next_index in adj_list[curr_index]:
        if not is_visited[next_index]:
            dfs_finish_order(next_index)
    finish_order.append(curr_index)          # strongly_connected_components.py:69  <- 늦게 끝날수록 뒤에 쌓임

# 2단계: 간선을 모두 뒤집은 그래프 생성
reversed_adj_list[next_index].append(curr_index)   # strongly_connected_components.py:78

# 3단계: finish_order의 역순으로, 뒤집은 그래프에서 다시 DFS
for curr_index in reversed(finish_order):     # strongly_connected_components.py:88
    if not is_visited[curr_index]:
        ...  # 이번에 한 번의 dfs_collect 호출로 방문되는 노드 전체가 하나의 SCC
```

**왜 이렇게 하면 SCC가 나올까?** 원래 그래프에서 가장 늦게 끝난 노드는 (직관적으로) 다른 SCC들의 "가장 앞쪽"에 위치할 가능성이 높은 노드입니다. 이 노드부터 뒤집힌 그래프에서 DFS를 시작하면, 원래 그래프에서 이 노드로 "들어올 수 있었던" 노드들만 뒤집힌 그래프에서 "이 노드에서 나갈 수 있는" 노드가 되어 탐색됩니다. 서로 다른 SCC로 가는 간선은 뒤집혀도 여전히 한쪽 방향으로만 나 있으므로, 한 번의 `dfs_collect` 호출은 절대 다른 SCC로 새어나가지 않고 정확히 하나의 SCC 안에서만 머무릅니다.

## 4. 같은 그래프, 다른 순회 — 결과 비교

```python
adj_list = [[1], [2], [0, 3], [4], [5], [3]]

0 ──► 1 ──► 2 ──► 3 ──► 4
▲           │     ▲     │
└───────────┘     └─────┘
```

두 SCC는 `{0, 1, 2}`(2에서 0으로 되돌아가는 사이클)와 `{3, 4, 5}`(3→4→5→3 사이클)이고, 둘 사이를 잇는 `2 → 3` 간선은 한쪽 방향뿐이라 다리(bridge) 역할만 합니다.

| 구현 | 결과 |
|---|---|
| `scc_by_tarjan` | `[[2, 1, 0], [5, 4, 3]]` |
| `scc_by_kosaraju` | `[[0, 2, 1], [3, 5, 4]]` |

각 SCC 안의 노드 순서, SCC가 반환되는 순서는 알고리즘마다(그리고 인접 리스트에 노드가 나열된 순서에 따라) 다를 수 있지만, **"어떤 노드들이 같은 그룹으로 묶이는가"는 항상 동일**합니다. `test_strongly_connected_components.py`의 `as_component_set()` 헬퍼가 SCC 결과를 "그룹의 집합"으로 정규화해서 비교하는 이유가 여기 있습니다.

## 5. 시간복잡도 / 공간복잡도

| 항목 | Tarjan | Kosaraju |
|---|---|---|
| 시간복잡도 | `O(V + E)` | `O(V + E)` (DFS 두 번 + 그래프 뒤집기) |
| 공간복잡도 | `O(V)` (`visit`, `low_link`, `on_stack`, 스택) | `O(V + E)` (뒤집은 그래프를 별도로 저장) |
| DFS 호출 횟수 | 1번 | 2번 |
| 필요한 보조 개념 | discovery time, low-link ([단절점/단절선](../articulation/README.md)과 동일한 도구) | finish order ([위상 정렬의 DFS 기반 구현](../topological_sort/README.md)과 같은 개념) |

두 알고리즘 모두 점근적 시간복잡도는 같지만, Tarjan은 DFS를 한 번만 돌고 그래프를 뒤집지 않아도 되어 실무에서 조금 더 선호되는 편입니다. 반면 Kosaraju는 "끝난 순서 기록 → 그래프 뒤집기 → 역순 DFS"라는 단계가 명확히 분리되어 있어 원리를 이해하기는 더 쉽습니다.

## 6. 개념 ↔ 코드 대응표

| 개념 | 코드 위치 |
|---|---|
| Tarjan SCC 진입점 | `scc_by_tarjan()` (`strongly_connected_components.py:1`) |
| discovery time / low-link | `visit`, `low_link` (`strongly_connected_components.py:8-9`) |
| 현재 DFS 스택에 남아있는지 추적 | `on_stack` (`strongly_connected_components.py:10`) |
| SCC 루트 판별 후 스택에서 꺼내 묶기 | `if low_link[curr_index] == visit[curr_index]:` (`strongly_connected_components.py:33-40`) |
| Kosaraju SCC 진입점 | `scc_by_kosaraju()` (`strongly_connected_components.py:49`) |
| 1단계: 끝난 순서 기록 | `dfs_finish_order()` (`strongly_connected_components.py:59-66`) |
| 2단계: 그래프 뒤집기 | `reversed_adj_list` 생성 (`strongly_connected_components.py:75-78`) |
| 3단계: 역순으로 뒤집은 그래프에서 SCC 수집 | `dfs_collect()` (`strongly_connected_components.py:86-90`) |

## 7. 직접 실행해보기

`strongly_connected_components.py`에는 `if __name__ == '__main__':` 데모 블록이 없습니다. 아래처럼 직접 호출해볼 수 있습니다.

```bash
pytest tests/strong_connected_components/test_strongly_connected_components.py -v
```

```bash
python3 -c "
from algorithm.strong_connected_components.strongly_connected_components import scc_by_tarjan, scc_by_kosaraju

adj_list = [[1], [2], [0, 3], [4], [5], [3]]
print('tarjan  :', scc_by_tarjan(adj_list))
print('kosaraju:', scc_by_kosaraju(adj_list))
"
```

출력:

```
tarjan  : [[2, 1, 0], [5, 4, 3]]
kosaraju: [[0, 2, 1], [3, 5, 4]]
```

---

[◀ 이전: 위상 정렬](../topological_sort/README.md) | [다음: 유니온-파인드 ▶](../union_find/README.md)
