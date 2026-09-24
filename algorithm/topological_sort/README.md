# 위상 정렬 (Topological Sort)

> 구현: [`topological_sort.py`](./topological_sort.py) — `topological_sort_by_dfs_recursive()`, `topological_sort_by_indegree()`
> 관련 테스트: [`test_topological_sort.py`](../../tests/topological_sort/test_topological_sort.py)
> 이 문서를 읽기 전에 [BFS](../bfs/README.md), [DFS](../dfs/README.md) 문서를 먼저 읽는 것을 권장합니다.

## 1. 왜 위상 정렬이 필요한가?

대학교 수강신청을 떠올려보세요. "자료구조"를 듣기 전에 "프로그래밍 입문"을 먼저 들어야 하고, "알고리즘"을 듣기 전에 "자료구조"를 먼저 들어야 합니다. 이런 "선행 조건(prerequisite)" 관계를 만족하면서 전체 과목을 어떤 순서로 들어야 하는지 정하는 문제가 바로 **위상 정렬**입니다.

```
프로그래밍 입문 ──► 자료구조 ──► 알고리즘
                        │
                        └──► 데이터베이스
```

이 그래프에서 "자료구조"는 "프로그래밍 입문" 뒤, "알고리즘"과 "데이터베이스"보다 앞에 와야 합니다. 위상 정렬은 이렇게 **"A가 끝나야 B를 시작할 수 있다"는 방향이 있는 의존 관계**를 모두 만족하는 하나의 순서를 찾아줍니다. 빌드 도구가 소스 파일 간 컴파일 순서를 정하거나, 작업 스케줄러가 태스크 실행 순서를 정할 때도 똑같은 원리가 쓰입니다.

## 2. 왜 DAG(방향 비순환 그래프)에서만 가능한가?

위상 정렬이 성립하려면 그래프에 **사이클(cycle)이 없어야** 합니다. 만약 "A는 B보다 먼저" 이면서 동시에 "B는 A보다 먼저"인 사이클이 있다면, 둘 중 어느 것도 먼저 놓을 수 없기 때문입니다.

```
   A ──► B
   ▲     │
   └─────┘
```

`A → B → A`라는 사이클이 있으면 "A가 B보다 앞선다"와 "B가 A보다 앞선다"가 동시에 요구되어 모순입니다. 그래서 위상 정렬은 **DAG(Directed Acyclic Graph, 방향 비순환 그래프)** 에서만 정의됩니다. 이 저장소의 두 구현 모두 사이클이 있으면 정렬을 완성하지 못하고 `has_cycle=True`를 반환합니다.

## 3. 두 가지 구현: Kahn 알고리즘 vs DFS 기반

이 저장소는 위상 정렬을 구현하는 두 가지 고전적인 방법을 모두 제공합니다.

### 3-1. Kahn 알고리즘 (진입차수 기반) — `topological_sort_by_indegree()`

**핵심 아이디어**: "아무도 나를 가리키지 않는(선행 조건이 없는) 노드부터" 순서대로 뽑아냅니다. 한 노드를 뽑아 결과에 넣을 때마다, 그 노드가 가리키던 이웃들의 **진입차수(in-degree, 나를 가리키는 간선의 개수)** 를 하나씩 줄이고, 진입차수가 0이 된 노드를 큐에 새로 추가합니다. 이는 BFS와 구조가 매우 비슷합니다([`../bfs/README.md`](../bfs/README.md) 참고).

```python
in_degree = [0] * len(adj_list)                 # topological_sort.py:35
for indices in adj_list:
    for index in indices:
        in_degree[index] += 1                    # 각 노드를 가리키는 간선 수 세기

queue = deque()
for index in range(len(in_degree)):
    if in_degree[index] == 0:                     # topological_sort.py:43  <- 선행 조건이 없는 노드부터
        queue.append(index)

while queue:
    curr_index = queue.popleft()
    sorted_result.append(curr_index)

    for next_index in adj_list[curr_index]:
        in_degree[next_index] -= 1                # topological_sort.py:52  <- "선행 조건 하나 해소"
        if in_degree[next_index] == 0:
            queue.append(next_index)               # topological_sort.py:55  <- 이제 선행 조건이 다 해소됨

has_cycle = len(sorted_result) < len(adj_list)      # topological_sort.py:57
```

**사이클 판정**: 사이클에 속한 노드는 진입차수가 절대 0이 되지 않으므로 큐에 들어오지 못합니다. 그래서 `sorted_result`에 담긴 노드 수가 전체 노드 수보다 적다면(`topological_sort.py:57`) 사이클이 있다는 뜻입니다.

### 3-2. DFS 기반 — `topological_sort_by_dfs_recursive()`

**핵심 아이디어**: 각 노드에서 DFS로 갈 수 있는 데까지 깊게 들어갔다가, **더 이상 갈 곳이 없어 완전히 끝난(finish) 노드부터** 스택에 쌓습니다. 모든 노드의 탐색이 끝난 뒤 스택을 뒤집으면 위상 정렬 순서가 됩니다.

이를 위해 노드마다 두 가지 상태를 추적합니다(`topological_sort.py:5-6`).

| 상태 | 의미 | 색으로 비유하면 |
|---|---|---|
| `is_visited=False` | 아직 방문 전 | 흰색(white) |
| `is_visited=True`, `is_finished=False` | 방문했지만 아직 처리 중 (지금 이 노드에서 시작된 DFS 호출이 재귀 스택 위에 살아있음) | 회색(gray) |
| `is_finished=True` | 이 노드와 그 아래 서브트리를 모두 처리 완료 | 검정(black) |

```python
def dfs(adj_list, curr_index, is_visited, is_finished, result):
    nonlocal has_cycle
    is_visited[curr_index] = True                    # topological_sort.py:11  <- 흰색 -> 회색

    for next_index in adj_list[curr_index]:
        if not is_visited[next_index]:
            dfs(adj_list, next_index, is_visited, is_finished, result)
        elif not is_finished[next_index]:              # topological_sort.py:16  <- 회색 노드를 다시 가리킴!
            has_cycle = True                            # topological_sort.py:17
            return

    is_finished[curr_index] = True                    # topological_sort.py:20  <- 회색 -> 검정
    result.append(curr_index)                          # topological_sort.py:21  <- 끝난 순서대로 쌓기
```

**사이클 판정**: `next_index`가 이미 `is_visited=True`인데 아직 `is_finished=False`(회색)라면, 이는 "지금 재귀 스택 위에 살아있는 조상 노드를 다시 가리키는 간선"을 만난 것입니다. 이런 간선을 **역방향 간선(back edge)** 이라 부르며, 역방향 간선이 하나라도 있으면 반드시 사이클이 존재합니다(`topological_sort.py:16-18`).

마지막으로, 완료된 순서(끝난 노드부터 쌓인 스택)를 뒤집으면 위상 정렬 순서가 됩니다(`topological_sort.py:27-30`). "가장 늦게 끝나는 노드가 가장 먼저 와야 한다"는 점이 핵심입니다 — 의존하는 노드가 많은(자식이 많은) 노드일수록 모든 자식이 끝나야 자신도 끝나므로, 늦게 끝날수록 더 앞선 위상 순서를 가집니다.

## 4. 같은 그래프, 다른 결과 — 위상 정렬은 정답이 여러 개일 수 있다

```
adj_list = [[1, 2], [3], [2], []]

        0
       / \
      1   2
       \ /
        ▼
        3   (2도 3을 가리킴: [[1, 2], [3], [3], []] 형태의 그래프 예시)
```

아래는 `[[1, 2], [3], [3], []]` 그래프에 대해 두 구현을 실제로 실행한 결과입니다.

| 구현 | 결과 순서 |
|---|---|
| `topological_sort_by_dfs_recursive` | `[0, 2, 1, 3]` |
| `topological_sort_by_indegree` (Kahn) | `[0, 1, 2, 3]` |

두 결과가 다르지만 **둘 다 정답**입니다. "0은 1과 2보다 앞서야 하고, 1과 2는 모두 3보다 앞서야 한다"는 조건만 만족하면 되고, 1과 2 사이의 순서는 애초에 정해져 있지 않기 때문입니다(위상 정렬은 유일한 정답이 아니라 조건을 만족하는 "하나의" 순서를 찾는 문제입니다). `test_topological_sort.py:14-18`의 `assert_valid_topological_order()`가 "정확한 순서 하나"가 아니라 "간선 방향을 만족하는지"만 검증하는 이유가 여기에 있습니다.

## 5. 시간복잡도 / 공간복잡도

| 항목 | Kahn (진입차수) | DFS 기반 |
|---|---|---|
| 시간복잡도 | `O(V + E)` | `O(V + E)` |
| 공간복잡도 | `O(V)` (`in_degree` 배열 + 큐) | `O(V)` (`is_visited`, `is_finished` 배열 + 재귀 스택) |
| 사이클 판정 방법 | 결과 개수가 전체 노드 수보다 적은지 확인 | 역방향 간선(back edge) 존재 여부 확인 |
| 재귀 깊이 제약 | 없음 | 그래프가 깊으면 파이썬 재귀 한도에 걸릴 수 있음 (DFS와 동일한 특성 — [`../dfs/README.md`](../dfs/README.md#5-시간복잡도--공간복잡도) 참고) |

## 6. 개념 ↔ 코드 대응표

| 개념 | 코드 위치 |
|---|---|
| DFS 기반 위상 정렬 진입점 | `topological_sort_by_dfs_recursive()` (`topological_sort.py:3`) |
| 흰색/회색/검정 상태 추적 | `is_visited`, `is_finished` (`topological_sort.py:5-6`) |
| 역방향 간선(사이클) 탐지 | `elif not is_finished[next_index]: has_cycle = True` (`topological_sort.py:16-17`) |
| 완료 순서를 뒤집어 위상 순서 만들기 | `while stack: sorted_result.append(stack.pop())` (`topological_sort.py:28-29`) |
| Kahn 알고리즘 진입점 | `topological_sort_by_indegree()` (`topological_sort.py:34`) |
| 진입차수 계산 | `in_degree[index] += 1` (`topological_sort.py:37-39`) |
| 진입차수 0인 노드부터 큐에 투입 | `topological_sort.py:41-44` |
| 간선 소비 후 진입차수 0이면 큐에 추가 | `topological_sort.py:51-55` |
| 사이클 판정 (Kahn) | `has_cycle = len(sorted_result) < len(adj_list)` (`topological_sort.py:57`) |

## 7. 직접 실행해보기

`topological_sort.py`에는 `if __name__ == '__main__':` 데모 블록이 없습니다. 아래처럼 직접 호출해볼 수 있습니다.

```bash
pytest tests/topological_sort/test_topological_sort.py -v
```

```bash
python3 -c "
from algorithm.topological_sort.topological_sort import (
    topological_sort_by_dfs_recursive,
    topological_sort_by_indegree,
)

adj_list = [[1, 2], [3], [3], []]
print('dfs_recursive:', topological_sort_by_dfs_recursive(adj_list))
print('indegree     :', topological_sort_by_indegree(adj_list))

# 사이클이 있는 그래프
cyclic = [[1], [2], [0]]
print('cyclic graph :', topological_sort_by_indegree(cyclic))
"
```

출력:

```
dfs_recursive: ([0, 2, 1, 3], False)
indegree     : ([0, 1, 2, 3], False)
cyclic graph : ([], True)
```

---

[◀ 이전: Floyd-Warshall 모든 쌍 최단 경로](../floyd_warshall/README.md) | [다음: 강한 연결 요소 (SCC) ▶](../strong_connected_components/README.md)
