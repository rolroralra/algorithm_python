# Dijkstra 최단 경로 알고리즘 (Dijkstra's Shortest Path)

> 구현: [`dijkstra.py`](./dijkstra.py) — `dijkstra_by_priority_queue()`, `dijkstra_by_heapq()`, `shortest_path()`
> 관련 테스트: [`test_dijkstra.py`](../../tests/dijkstra/test_dijkstra.py)
> 이 문서를 읽기 전에 [BFS 문서](../bfs/README.md)를 먼저 읽는 것을 권장합니다.

## 1. 왜 Dijkstra가 필요한가?

BFS는 "간선이 모두 동일한 비용(1칸)"일 때 최단 경로를 찾습니다. 하지만 현실의 길찾기는 그렇지 않습니다. 지도 앱에서 "가장 빠른 길"을 찾을 때는 도로마다 거리(혹은 소요 시간)가 다르고, 항공편 요금 비교에서는 구간마다 가격이 다릅니다. **간선마다 서로 다른(0 이상의) 가중치가 있는 그래프에서 최단 경로를 찾는 것**이 Dijkstra 알고리즘의 역할입니다.

```
        1         2
   0 ───────► 1 ───────► 2
    \                    ▲
     \________4_________/        0 -> 2로 가는 두 가지 경로
                                  - 직접: 4
                                  - 0→1→2: 1+2 = 3  (더 짧음!)
```

Dijkstra는 **"아직 확정되지 않은 노드 중 지금까지 알려진 거리가 가장 짧은 노드부터 확정한다"** 는 탐욕(greedy) 전략을 사용합니다. "가장 가까운 곳부터 순서대로 방문한다"는 점에서 BFS와 철학이 비슷하지만, BFS의 큐 대신 "가장 짧은 거리"를 기준으로 꺼내는 **우선순위 큐(Priority Queue)** 를 사용한다는 점이 다릅니다.

## 2. 핵심 아이디어: 우선순위 큐(heapq)로 "가장 가까운 곳"부터 확정하기

BFS의 큐는 "먼저 들어온 순서"대로 꺼내지만, Dijkstra는 "지금까지 알려진 거리가 가장 짧은 노드"를 꺼내야 합니다. 이를 위해 이 저장소는 두 가지 우선순위 큐 구현을 모두 제공합니다.

| 구현 | 사용 모듈 | 특징 |
|---|---|---|
| `dijkstra_by_priority_queue()` (`dijkstra.py:5`) | `queue.PriorityQueue` | 내부에 락(lock)이 있어 스레드 안전(thread-safe)하지만, 단일 스레드에서는 그만큼 오버헤드가 있음 |
| `dijkstra_by_heapq()` (`dijkstra.py:35`) | `heapq` | 락이 없는 가벼운 이진 힙(binary heap). 단일 스레드 환경에서 더 가볍고 빠름 |

두 구현은 내부 자료구조만 다를 뿐 로직은 동일하며, `test_dijkstra.py:57-61`의 `test_both_implementations_agree_on_distances`가 두 결과가 항상 같음을 검증합니다.

### 왜 `heapq`(최소 힙)를 쓰는가?

배열에서 매번 "가장 작은 값"을 선형 탐색으로 찾으면 `O(V)`가 걸리고, 이를 V번 반복하면 `O(V²)`가 됩니다. 최소 힙을 쓰면 "가장 작은 값 꺼내기"와 "새 값 넣기"가 모두 `O(log V)`라서, 전체 알고리즘을 `O(E log V)`로 줄일 수 있습니다.

## 3. 코드로 보는 Dijkstra 동작

```python
distance[start_index] = 0                              # dijkstra.py:43
heapq.heappush(priority_queue, (0, start_index))        # dijkstra.py:44

while priority_queue:
    curr_distance, curr_index = heapq.heappop(priority_queue)  # dijkstra.py:47

    if is_visited[curr_index]:          # dijkstra.py:49  <- "지연 삭제(lazy deletion)"
        continue
    is_visited[curr_index] = True       # dijkstra.py:52  <- 이 순간 curr_index의 최단 거리가 "확정"됨

    for next_index, edge_length in adj_list[curr_index]:
        next_distance = distance[curr_index] + edge_length
        if next_distance < distance[next_index]:         # 더 짧은 길을 찾으면
            distance[next_index] = next_distance          # 갱신(relax)
            prev_index[next_index] = curr_index
            heapq.heappush(priority_queue, (distance[next_index], next_index))
```

### 지연 삭제(lazy deletion)란?

힙에는 "삭제"나 "우선순위 갱신" 연산이 기본으로 없기 때문에, 이미 큐에 들어있는 `(거리, 노드)` 항목을 지우는 대신 **더 짧은 거리를 찾을 때마다 새 항목을 그냥 추가로 push**합니다(`dijkstra.py:60`). 그러면 같은 노드가 힙에 여러 번 들어있을 수 있는데, 이미 `is_visited`로 확정된 노드를 나중에 다시 꺼내면 `dijkstra.py:49`에서 `continue`로 건너뛰어 무시합니다. "삭제 대신 무시"하는 전략이라서 지연 삭제라고 부릅니다.

## 4. 왜 음수 가중치에서는 동작하지 않는가?

Dijkstra의 핵심 전제는 **"한 번 확정(방문)한 노드의 최단 거리는 이후 어떤 경로로도 더 줄어들 수 없다"** 는 것입니다. 이는 모든 간선 가중치가 0 이상일 때만 성립합니다. 음수 간선이 있으면 "이미 확정한 노드"를 나중에 더 짧게 만드는 경로가 나타날 수 있는데, Dijkstra는 확정된 노드는 다시 꺼내 검토하지 않으므로 잘못된 결과를 낼 수 있습니다.

실제로 이 저장소의 코드로 재현해보면:

```python
graph = [
    [(1, 1), (2, 2)],   # 0 -> 1 (가중치 1), 0 -> 2 (가중치 2)
    [(3, 100)],          # 1 -> 3 (가중치 100)
    [(1, -10)],           # 2 -> 1 (가중치 -10)
    [],
]
dijkstra_by_heapq(graph, 0)
```

```
        1              100
   0 ───────► 1 ───────────────► 3
    \         ▲
     \2       │ -10
      \       │
       ▼      │
        2 ────┘
```

| 알고리즘 | 결과 `distance` | 정확성 |
|---|---|---|
| `dijkstra_by_heapq` | `[0, -8, 2, 101]` | 3번 노드 값(`101`)이 틀림 |
| `bellman_ford` (참고) | `[0, -8, 2, 92]` | 정확함 (`92 = -8 + 100`) |

무슨 일이 벌어진 걸까요?

1. 힙에서 `(1, 1)`이 `(2, 2)`보다 먼저 꺼내져 **노드 1이 거리 1로 먼저 확정**됩니다(`is_visited[1] = True`).
2. 노드 1이 확정된 그 순간, 노드 1의 이웃인 노드 3의 거리가 `1 + 100 = 101`로 계산되어 큐에 들어갑니다.
3. 뒤이어 노드 2가 확정되면서, `2 → 1` 간선(가중치 `-10`)을 통해 `distance[1]`이 `2 + (-10) = -8`로 더 짧게 갱신됩니다. 하지만 노드 1은 **이미 확정된 뒤**라서 이 갱신은 "노드 1에서 출발하는 다른 경로들"에는 전혀 반영되지 못합니다.
4. 결국 노드 3은 "진짜 최단 거리로 갱신되기 전의, 확정 당시의 노드 1"(거리 1)을 기준으로 계산된 `101`을 그대로 가지게 됩니다. 진짜 최단 거리는 `-8 + 100 = 92`입니다.

이처럼 **음수 간선은 "이미 확정한 노드가 더 짧아질 수 있다"는 모순을 만들기 때문에** Dijkstra의 탐욕 전제가 깨집니다.

## 5. Dijkstra vs Bellman-Ford 비교

| 구분 | Dijkstra | Bellman-Ford |
|---|---|---|
| 음수 가중치 | 지원 안 함 (위 예시처럼 잘못된 결과) | 지원함 |
| 음수 사이클 탐지 | 불가능 | 가능 |
| 시간복잡도 | `O(E log V)` (힙 사용 시) | `O(V · E)` |
| 핵심 자료구조 | 우선순위 큐(최소 힙) | 없음 (단순 반복문) |
| 전략 | 탐욕(greedy) — 가장 가까운 노드부터 확정 | 동적 계획법에 가까움 — 모든 간선을 V-1번 반복 이완(relax) |

가중치가 모두 0 이상이라고 보장된다면 Dijkstra가 더 빠르고, 음수 가중치가 있을 수 있다면 Bellman-Ford를 써야 합니다. 자세한 내용은 [`../bellman_ford/README.md`](../bellman_ford/README.md)를 참고하세요.

## 6. 시간복잡도 / 공간복잡도

| 항목 | 복잡도 | 설명 |
|---|---|---|
| 시간복잡도 | `O(E log V)` | 각 간선마다 최대 한 번 `heappush`(`O(log V)`), 각 정점마다 최대 한 번 `heappop` |
| 공간복잡도 | `O(V + E)` | `distance`, `prev_index`, `is_visited` 배열 (`O(V)`) + 힙에 최대 `O(E)`개 항목 |

## 7. 개념 ↔ 코드 대응표

| 개념 | 코드 위치 |
|---|---|
| 우선순위 큐 버전 (`queue.PriorityQueue`) | `dijkstra_by_priority_queue()` (`dijkstra.py:5`) |
| 최소 힙 버전 (`heapq`) | `dijkstra_by_heapq()` (`dijkstra.py:35`) |
| 시작 정점 거리 0으로 초기화 | `distance[start_index] = 0` (`dijkstra.py:13`, `43`) |
| 지연 삭제(이미 확정된 노드 무시) | `if is_visited[curr_index]: continue` (`dijkstra.py:19`, `49`) |
| 간선 이완(relaxation) | `if next_distance < distance[next_index]:` (`dijkstra.py:27`, `57`) |
| 경로 역추적 | `shortest_path()` (`dijkstra.py:65`) |

## 8. 직접 실행해보기

`dijkstra.py`에는 `if __name__ == '__main__':` 데모 블록이 없습니다. 아래처럼 직접 호출해볼 수 있습니다.

```bash
pytest tests/dijkstra/test_dijkstra.py -v
```

```bash
python3 -c "
from algorithm.dijkstra.dijkstra import dijkstra_by_heapq, shortest_path

graph = [[(1, 1), (2, 4)], [(2, 2)], [(3, 1)], []]
distance, prev_index = dijkstra_by_heapq(graph, 0)
print('distance:', distance)
print('0 -> 3 경로:', shortest_path(prev_index, 3))
"
```

출력:

```
distance: [0, 1, 3, 4]
0 -> 3 경로: [0, 1, 2, 3]
```

---

[◀ 이전: DFS (깊이 우선 탐색)](../dfs/README.md) | [다음: Bellman-Ford 최단 경로 ▶](../bellman_ford/README.md)
