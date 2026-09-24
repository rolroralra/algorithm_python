# 단절선 (Articulation Edge / Bridge)

> 구현: [`articulation_edge.py`](./articulation_edge.py) — `articulation_edges()`
> 이 문서를 읽기 전에 [ARTICULATION_POINT.md](./ARTICULATION_POINT.md)를 먼저 읽어주세요. discovery time, low-link, DFS spanning tree 개념을 그대로 이어서 사용합니다.

## 1. 단절점 코드와 무엇이 다른가?

뼈대(DFS + discovery time + low-link)는 단절점 알고리즘과 완전히 같습니다. 하지만 `articulation_edge.py`의 `dfs()`는 두 가지 지점에서 명확히 다르게 동작합니다.

```python
def dfs(curr_index: int, prev_index: int = -1) -> int:
    if visit[curr_index] > 0:
        return visit[curr_index]

    visit[curr_index] = visit_seq
    visit_seq += 1
    min_visit_seq = visit[curr_index]

    for next_index in adj_list[curr_index]:
        if next_index == prev_index:
            continue                                          # ① 부모로 되돌아가는 간선은 완전히 건너뛴다

        if visit[next_index] == 0:
            min_visit_seq_from_child = dfs(next_index, curr_index)

            if min_visit_seq_from_child > visit[curr_index]:    # ② 엄격한 '>' 비교
                articulation_edge = (curr_index, next_index) if curr_index <= next_index else (next_index, curr_index)
                articulation_edge_list.append(articulation_edge)
        else:
            min_visit_seq_from_child = visit[next_index]

        min_visit_seq = min(min_visit_seq, min_visit_seq_from_child)

    return min_visit_seq
```
(`articulation_edge.py:8-35`)

## 2. 차이점 ① — 부모로 되돌아가는 간선을 명시적으로 건너뛴다

`dfs(curr_index, prev_index=-1)`는 "내가 어떤 간선을 타고 여기 왔는지"(`prev_index`)를 인자로 받아서 기억합니다. 그리고 이웃을 순회할 때 `next_index == prev_index`이면 **그 간선을 아예 보지 않고 건너뜁니다**(`articulation_edge.py:20-22`).

반면 [단절점 코드](./ARTICULATION_POINT.md)의 `dfs(curr_index, is_root=False)`는 `prev_index`를 따로 받지 않으므로, 부모로 되돌아가는 간선도 "이미 방문한 노드로의 역방향 간선"으로 취급해서 그대로 low-link 계산에 포함시킵니다.

**왜 단절선 판정에서는 반드시 건너뛰어야 할까?** 다리(bridge) 여부는 "이 **간선 하나**를 지웠을 때 끊어지는가"를 묻습니다. 만약 부모로 되돌아가는 그 간선 자체를 자기 자신의 low-link 계산에 포함시켜 버리면, 모든 트리 간선이 "내 부모의 discovery time에 도달 가능"이라는 자명한(trivial) 사실만으로 `low[child] <= discovery[curr]`가 항상 성립해버립니다. 그러면 어떤 간선도 다리로 판정될 수 없게 되어 알고리즘이 무의미해집니다. 그래서 단절선을 찾을 때는 "내가 타고 온 바로 그 간선"은 계산에서 제외하고, **다른 경로(back edge)로 조상에 닿을 수 있는지만** 따져야 합니다.

## 3. 차이점 ② — 비교 연산자가 `>=`가 아니라 `>` (엄격한 부등호)

| | 단절점 (`articulation_point.py:35`) | 단절선 (`articulation_edge.py:27`) |
|---|---|---|
| 조건 | `low[child] >= discovery[curr]` | `low[child] > discovery[curr]` |
| 판정 대상 | 정점 `curr` | 간선 `(curr, child)` |

**직관**: `low[child] == discovery[curr]`인 경우, 즉 `child`의 서브트리에서 `curr` 자신으로 곧장 돌아오는 역방향 간선이 있는 경우를 생각해봅시다.

- **정점 `curr`를 지우는 경우**: `curr` 자신이 사라지므로, 그 역방향 간선의 도착지(`curr`)도 함께 사라집니다. `child`의 서브트리는 여전히 고립됩니다 → `curr`는 단절점이 **맞습니다** → `>=`(같아도 단절점)
- **간선 `(curr, child)`만 지우는 경우**: `curr`는 그대로 남아있으므로, `child`의 서브트리는 그 역방향 간선을 통해 여전히 `curr`(그리고 나머지 그래프)에 연결되어 있습니다 → `(curr, child)`는 다리가 **아닙니다** → 반드시 `>`(같으면 다리 아님)

```
      curr
     /    \
  child    (다른 이웃)
     \
      ╰╌╌╌╌╌╌╮  (역방향 간선: child의 서브트리 → curr)
             curr

low[child] == discovery[curr] 인 상황:
 - curr 제거 시: child 쪽 서브트리 고립 → curr = 단절점 (>= 조건 만족)
 - 간선(curr,child) 만 제거 시: 위의 역방향 간선으로 여전히 연결됨 → 다리 아님 (> 조건 불만족, 정확히 맞음)
```

## 4. 루트 특수 케이스가 필요 없는 이유

단절점 코드는 `is_root`를 받아 "자식이 2개 이상이면 단절점"이라는 별도 규칙을 두었습니다([ARTICULATION_POINT.md 4장](./ARTICULATION_POINT.md#4-루트-노드의-특수-케이스-왜-자식이-2개-이상이면-단절점인가) 참고). 하지만 `articulation_edges()`의 진입점(`articulation_edge.py:37-39`)은 `is_root` 같은 매개변수 없이 그냥 `dfs(i)`를 호출합니다.

```python
for i in range(V):
    if visit[i] == 0:
        dfs(i)
```
(`articulation_edge.py:37-39`)

다리 판정은 항상 **트리 간선 하나(`curr`—`child`)** 를 기준으로 `low[child] > discovery[curr]`를 검사합니다. 이 비교는 `curr`가 루트든 아니든 그대로 의미가 있습니다 — 루트도 자기 자신의 discovery time(예: 1)을 가지고 있고, 루트에서 뻗어나간 트리 간선도 "그 간선을 지우면 자식 서브트리가 고립되는가"라는 질문에 똑같이 답할 수 있기 때문입니다. 단절점처럼 "비교할 조상이 없다"는 문제 자체가 애초에 생기지 않으므로 특수 케이스가 필요 없습니다.

## 5. 예시로 직접 비교해보기 (README의 공통 그래프)

같은 그래프(삼각형 `0-1-2` + 다리 `1-3` + 펜던트 `3-4`)를 두 알고리즘에 각각 돌리면, **부모 간선 처리 방식이 다르기 때문에 중간 low-link 값이 달라집니다** — 하지만 최종 결과(단절점 `{1,3}`, 단절선 `{(1,3),(3,4)}`)는 두 알고리즘이 서로 일관된 답을 냅니다.

```
정점 4 (펜던트 끝, 부모는 3):

  단절점 코드: 부모(3)로의 역방향 간선도 포함 → low[4] = min(discovery[4], discovery[3]) = min(5, 4) = 4
  단절선 코드: 부모(3)로의 간선은 건너뜀      → low[4] = discovery[4] = 5   (다른 이웃이 없으므로)

  단절점 판정: low[4]=4 >= discovery[3]=4 → True → 3은 단절점
  단절선 판정: low[4]=5 >  discovery[3]=4 → True → (3,4)는 다리
```

두 쪽 다 "4는 3을 거치지 않고는 아무 데도 못 간다"는 같은 사실을 말하고 있지만, 단절점 쪽은 `low[4]`가 부모(3)의 discovery time까지 자연스럽게 낮아지는 것을 허용한 뒤 `>=`로 "같아도 인정"하고, 단절선 쪽은 부모 간선 자체를 아예 배제한 뒤 `>`로 "조금이라도 낮아지면 탈락"시키는, 서로 다른 방식으로 같은 결론에 도달합니다.

## 6. 시간/공간복잡도

| 항목 | 복잡도 |
|---|---|
| 시간 | `O(V + E)` |
| 공간 | `O(V)` — `visit` 배열 + 재귀 스택 |

## 7. 개념 ↔ 코드 대응표

| 개념 | 코드 위치 |
|---|---|
| 진입점 (모든 연결 요소를 순회, 루트 표시 불필요) | `for i in range(V): if visit[i] == 0: dfs(i)` (`articulation_edge.py:37-39`) |
| 부모 간선 추적 및 제외 | `dfs(curr_index, prev_index)` / `if next_index == prev_index: continue` (`articulation_edge.py:8`, `21-22`) |
| discovery time | `visit[]` (`articulation_edge.py:5`) |
| low-link 계산 및 반환 | `dfs()`의 반환값 `min_visit_seq` (`articulation_edge.py:18, 35`) |
| 단절선(다리) 판정 조건 (엄격한 `>`) | `articulation_edge.py:27` |
| 간선 정규화 (작은 인덱스 먼저) | `(curr_index, next_index) if curr_index <= next_index else (next_index, curr_index)` (`articulation_edge.py:28`) |

## 8. 직접 실행해보기

`articulation_edge.py`에는 `if __name__ == '__main__':` 데모 블록이 없습니다. pytest로 동작을 확인하거나, 아래처럼 직접 실습해볼 수 있습니다.

```bash
python3 -m pytest tests/articulation/test_articulation_edge.py -v
```

```python
from algorithm.articulation.articulation_edge import articulation_edges

# 삼각형 0-1-2, 다리 1-3, 펜던트 3-4
adj_list = [[1, 2], [0, 2, 3], [0, 1], [1, 4], [3]]
print(articulation_edges(adj_list))   # [(3, 4), (1, 3)] (발견 순서, 정렬되어 있지 않음)
```

---

이전 문서: [← 단절점 (Articulation Point)](./ARTICULATION_POINT.md)
다음 문서: 없음 (그래프 알고리즘 문서 시리즈 끝 — [인덱스로 돌아가기](./README.md))
