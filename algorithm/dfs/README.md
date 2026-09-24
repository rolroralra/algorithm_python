# DFS (깊이 우선 탐색, Depth-First Search)

> 구현: [`dfs.py`](./dfs.py) — `dfs()` 함수 (재귀 버전과 스택 버전을 모두 제공)
> 관련 테스트: [`test_dfs.py`](../../tests/dfs/test_dfs.py)
> 이 문서를 읽기 전에 [BFS 문서](../bfs/README.md)를 먼저 읽는 것을 권장합니다.

## 1. 왜 DFS가 필요한가?

미로를 풀 때 사람이 실제로 하는 행동을 떠올려보세요. 갈림길이 나오면 일단 **한쪽 방향으로 갈 수 있는 데까지 끝까지 가보고**, 막다른 길이면 바로 직전 갈림길로 되돌아와 다른 방향을 시도합니다. 이것이 바로 DFS(깊이 우선 탐색)의 동작 방식입니다.

```
        0
       / \
      1   2
      |   |
      3   4
```

BFS가 "물결처럼 레벨 단위로 퍼져나간다"면, DFS는 "한 줄기 길을 끝까지 파고들었다가, 막히면 되돌아온다(backtrack)"는 점이 다릅니다. 경로가 존재하는지 여부, 미로 탈출, 백트래킹 문제(스도쿠, N-Queen), 위상 정렬([`../topological_sort/README.md`](../topological_sort/README.md) 참고) 등 "일단 끝까지 가봐야 아는" 문제에 DFS가 자연스럽게 쓰입니다.

## 2. 핵심 아이디어: 스택(LIFO) 또는 재귀

"막히면 가장 최근에 갈라졌던 지점으로 되돌아간다"는 동작은 **LIFO(Last In First Out)**, 즉 스택과 정확히 같은 구조입니다. 그리고 재귀 함수 호출 역시 내부적으로 콜 스택(call stack)을 사용하므로, **재귀 호출 자체가 곧 스택 기반 DFS**입니다.

`dfs.py:1`의 `dfs()` 함수는 `recursive` 플래그로 두 가지 구현 중 하나를 선택합니다.

```python
def dfs(adjacent_list, is_visited, start_index=0, recursive=False):   # dfs.py:1
    if recursive:
        __dfs_by_recursive(adjacent_list, is_visited, start_index)     # dfs.py:4
    else:
        __dfs_smoothly_by_stack(adjacent_list, is_visited, start_index) # dfs.py:7
```

## 3. 코드로 보는 DFS 동작

같은 그래프 `[[1, 2], [0, 3], [0, 4], [1], [2]]`(BFS 문서와 동일)를 예로 들어보겠습니다.

### 재귀 버전 (`__dfs_by_recursive`, `dfs.py:47-56`)

```
0 방문 → 이웃 [1, 2] 중 1을 먼저 시도
  1 방문 → 이웃 [0, 3] 중 3을 시도 (0은 이미 방문)
    3 방문 → 이웃 [1] 모두 방문됨 → 되돌아감
  (1의 나머지 이웃 없음) → 되돌아감
(0의 다음 이웃) 2 방문 → 이웃 [0, 4] 중 4를 시도
  4 방문 → 이웃 [2] 모두 방문됨 → 되돌아감
```

방문 순서: **`0 → 1 → 3 → 2 → 4`**

### 스택 버전 (`__dfs_smoothly_by_stack`, `dfs.py:10-24`)

```python
stack = [start_index]              # dfs.py:11
is_visited[start_index] = True     # dfs.py:12

while stack:
    curr_index = stack.pop()       # dfs.py:15  <- 맨 뒤(가장 최근에 넣은 것)부터 꺼냄

    for next_index in adjacent_list[curr_index]:
        if is_visited[next_index]:
            continue
        stack.append(next_index)          # dfs.py:23
        is_visited[next_index] = True     # dfs.py:24  <- push할 때 표시 (BFS와 같은 패턴)
```

| 단계 | 스택 상태(처리 전) | pop한 노드 | 새로 push된 노드 |
|---|---|---|---|
| 1 | `[0]` | 0 | 1, 2 |
| 2 | `[1, 2]` | 2 | 4 |
| 3 | `[1, 4]` | 4 | (없음) |
| 4 | `[1]` | 1 | 3 |
| 5 | `[3]` | 3 | (없음) |

방문 순서: **`0 → 2 → 4 → 1 → 3`**

### ⚠️ 주의: 스택 기반 반복 DFS는 재귀 DFS와 방문 "순서"가 다를 수 있다

위 두 트레이스를 비교하면 재귀는 `0,1,3,2,4`, 스택은 `0,2,4,1,3`으로 **순서 자체가 다릅니다**. 둘 다 "DFS"이고 둘 다 모든 노드를 정확히 한 번씩 방문하지만, 스택은 이웃을 `push`한 순서의 **역순으로 `pop`** 되기 때문입니다. 즉 `[1, 2]`를 순서대로 push하면 나중에 넣은 `2`가 먼저 `pop`됩니다(재귀에서는 `1`이 먼저 처리됨). 그래서 실제 방문 순서(재귀와 동일한 순서)가 중요한 문제라면, 이웃 리스트를 **역순으로 push**하는 보정이 필요합니다.

`test_dfs.py:8-9`가 `recursive` 값을 `[False, True]`로 파라미터화해서 두 버전을 모두 테스트하는데, 검증 내용이 "모든 도달 가능한 노드가 방문되었는가"(`is_visited` 배열이 같은가)이지 "방문 순서가 같은가"는 아닌 이유가 바로 이것입니다.

### 참고: 세 번째 구현, `__dfs_exactly_by_stack` (`dfs.py:27-45`)

파일 안에는 `dfs()`에서 실제로 호출되지 않는 세 번째 함수가 하나 더 있습니다. 방문 표시를 **push할 때가 아니라 pop할 때** 하는 버전입니다.

```python
while stack:
    curr_index = stack.pop()
    if is_visited[curr_index]:      # pop된 뒤에야 방문 여부 확인
        continue
    is_visited[curr_index] = True   # dfs.py:37  <- pop할 때 표시
    for next_index in adjacent_list[curr_index]:
        if is_visited[next_index]:
            continue
        stack.append(next_index)    # 방문 표시 없이 그냥 push (중복 push 가능)
```

이 방식은 같은 노드가 스택에 중복으로 쌓일 수 있는 대신(메모리를 더 씁니다), 재귀 DFS와 더 가까운 방문 순서를 내는 경향이 있습니다. 현재 공개 함수인 `dfs()`는 이 구현을 사용하지 않지만, "언제 방문 표시를 하느냐"에 따라 동작이 어떻게 달라지는지 비교해보기 좋은 예시로 파일에 남아 있습니다.

## 4. BFS와 DFS 비교

| 구분 | BFS | DFS |
|---|---|---|
| 자료구조 | 큐 (FIFO) | 스택 (LIFO) 또는 재귀 |
| 탐색 방식 | 가까운 노드부터 레벨 단위로 | 한 방향으로 최대한 깊이 들어갔다가 되돌아옴 |
| 무가중치 그래프 최단 경로 | 보장됨 | 보장되지 않음 |
| 구현 난이도 | 큐 하나로 비교적 단순 | 재귀는 간단하지만 스택 구현 시 방문 순서에 주의 필요 |
| 메모리 사용 패턴 | 그래프가 넓게 퍼질수록(branching factor가 클수록) 큐가 커짐 | 그래프가 깊을수록 스택(또는 재귀 깊이)이 커짐 |
| 대표 용도 | 최단 경로, 레벨별 탐색 | 경로 존재 여부, 백트래킹, 위상 정렬, 사이클 탐지 |

두 알고리즘 모두 시간복잡도는 `O(V + E)`로 동일하지만, "어떤 순서로 방문하느냐"와 "어떤 자료구조를 쓰느냐"가 근본적인 차이입니다. BFS 쪽 설명은 [`../bfs/README.md`](../bfs/README.md)를 참고하세요.

## 5. 시간복잡도 / 공간복잡도

| 항목 | 복잡도 | 설명 |
|---|---|---|
| 시간복잡도 | `O(V + E)` | 모든 정점과 간선을 한 번씩 확인 |
| 공간복잡도 (재귀) | `O(V)` | 최악의 경우(일자로 이어진 그래프) 재귀 깊이가 V까지 커짐 → 파이썬 재귀 한도(`sys.setrecursionlimit`)에 주의 |
| 공간복잡도 (스택) | `O(V)` | `is_visited` 배열 + 스택에 쌓이는 노드 수 |

## 6. 개념 ↔ 코드 대응표

| 개념 | 코드 위치 |
|---|---|
| DFS 진입점 (재귀/반복 선택) | `dfs()` (`dfs.py:1`) |
| 반복(스택) 버전 — push할 때 방문 표시 | `__dfs_smoothly_by_stack()` (`dfs.py:10`) |
| 반복(스택) 버전 — pop할 때 방문 표시 (미사용, 비교용) | `__dfs_exactly_by_stack()` (`dfs.py:27`) |
| 재귀 버전 | `__dfs_by_recursive()` (`dfs.py:47`) |
| 방문 처리(현재는 빈 자리) | `# visit process` (`dfs.py:17`, `36`, `50`) |
| 실행 데모 | `if __name__ == '__main__':` (`dfs.py:59`) |

## 7. 직접 실행해보기

`dfs.py:59-66`에 데모 블록이 있습니다.

```bash
python3 -m algorithm.dfs.dfs
```

실행하면 다음과 같이 출력됩니다.

```
Calling Recursive DFS
[True, True, True, True, True]
```

`dfs.py:64`에서 `recursive=True`로 호출하기 때문에 "Calling Recursive DFS"가 출력되며, 그래프 `[[1, 2], [0, 3], [0, 4], [1], [2]]`의 모든 노드가 방문되어 `is_visited` 배열이 전부 `True`로 채워집니다.

테스트 실행:

```bash
pytest tests/dfs/test_dfs.py -v
```

---

[◀ 이전: BFS (너비 우선 탐색)](../bfs/README.md) | [다음: Dijkstra 최단 경로 ▶](../dijkstra/README.md)
