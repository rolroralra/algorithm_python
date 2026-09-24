# Bellman-Ford 최단 경로 알고리즘 (Bellman-Ford Shortest Path)

> 구현: [`bellman_ford.py`](./bellman_ford.py) — `bellman_ford()`, `shortest_path()`
> 관련 테스트: [`test_bellman_ford.py`](../../tests/bellman_ford/test_bellman_ford.py)
> 이 문서를 읽기 전에 [Dijkstra 문서](../dijkstra/README.md)를 먼저 읽는 것을 권장합니다.

## 1. 왜 Bellman-Ford가 필요한가?

[Dijkstra 문서](../dijkstra/README.md#4-왜-음수-가중치에서는-동작하지-않는가)에서 확인했듯, Dijkstra는 **"이미 확정한 노드는 다시 검토하지 않는다"** 는 탐욕적 전제 때문에 음수 가중치가 있으면 잘못된 결과를 낼 수 있습니다.

그런데 현실에는 음수 가중치가 의미를 갖는 상황이 있습니다. 예를 들어 "환율 차익거래(arbitrage)"를 그래프 문제로 바꾸면, 환전 비율의 로그값을 간선 가중치로 사용해서 "가중치의 합이 음수인 사이클 = 차익거래가 가능한 루프"를 찾는 문제가 됩니다. 이럴 때는 "확정한 노드도 필요하면 다시 갱신할 수 있는" 알고리즘이 필요하고, 이것이 Bellman-Ford입니다.

Bellman-Ford는 Dijkstra처럼 "가장 가까운 노드부터 똑똑하게 고르는" 대신, **모든 간선을 정해진 횟수만큼 우직하게 반복해서 검사**합니다. 느리지만 훨씬 더 안정적입니다.

## 2. 핵심 아이디어: 모든 간선을 V-1번 반복해서 이완(relax)하기

그래프에 정점이 `V`개 있다면, 사이클이 없는 최단 경로는 **간선을 최대 `V-1`개까지만** 지나갈 수 있습니다(정점을 한 번씩만 거친다고 가정하면 경로의 간선 수는 정점 수보다 1 적기 때문입니다). 그래서 모든 간선에 대해 "이 간선을 거치면 더 짧아지는가?"를 확인하는 이완(relaxation) 작업을 `V-1`번 반복하면, 이론상 모든 최단 거리가 확정됩니다.

```
distance[to] = min(distance[to], distance[from] + weight(from, to))
```

**코드 연결**: `bellman_ford.py:17-25`가 정확히 이 작업을 합니다.

```python
for loop_index in range(vertex_count):                    # bellman_ford.py:17  <- V번 반복
    for from_index, to_index, length in edge_list:         # bellman_ford.py:18  <- 모든 간선 검사
        if distance[from_index] < INF and distance[from_index] + length < distance[to_index]:
            distance[to_index] = distance[from_index] + length   # 이완(relax)
            prev_index[to_index] = from_index

            if loop_index == vertex_count - 1:              # bellman_ford.py:23
                has_negative_cycle = True                    # V번째 반복에서도 갱신이 일어나면 음수 사이클
                break
```

## 3. 왜 정확히 V번(V-1번 + 확인 1번) 반복하는가?

- **처음 `V-1`번**(`loop_index`가 `0`부터 `V-2`까지): 실제로 최단 거리를 계산하는 라운드입니다. 각 라운드마다 "적어도 하나의 최단 경로"가 한 칸씩 더 확정되므로, 가장 긴 최단 경로(간선 `V-1`개)도 `V-1`번째 라운드에서 완전히 확정됩니다.
- **마지막(`V`번째, `loop_index == vertex_count - 1`) 반복**: 만약 이 라운드에서도 여전히 거리가 줄어드는 간선이 있다면, 이는 "음수 사이클을 계속 돌수록 거리가 끝없이 줄어들 수 있다"는 뜻입니다. 사이클이 없는 그래프라면 `V-1`번으로 이미 수렴했어야 하므로, `V`번째에도 갱신이 일어난다는 것 자체가 **음수 사이클이 존재한다는 증거**입니다.

이 구현은 표준적인 "V-1번 이완 + 별도의 1번 사이클 검사"를 분리하지 않고, `range(vertex_count)`로 **V번을 반복하면서 마지막 회차의 갱신 여부로 음수 사이클을 함께 검사**하도록 합쳐놓았습니다(`bellman_ford.py:23-25`).

### 음수 사이클 탐지 예시

```python
edges = [(0, 1, 1), (1, 2, -3), (2, 0, 1)]   # test_bellman_ford.py:38
bellman_ford(edges, 0)
```

```
   0 ──1──► 1
   ▲         │
   │        -3
   1         │
   │         ▼
   └──────── 2
```

사이클 `0 → 1 → 2 → 0`의 가중치 합은 `1 + (-3) + 1 = -1`, 즉 음수입니다. 이 사이클을 돌 때마다 거리가 계속 줄어들기 때문에 "최단 거리"라는 개념 자체가 성립하지 않고, `has_negative_cycle`이 `True`가 됩니다.

> 구현 참고: `vertex_count`는 간선 목록에 등장한 정점 번호들을 모아(`bellman_ford.py:4-9`) 그 개수로 정합니다. 정점 번호가 `0`부터 `V-1`까지 빠짐없이 연속된다고 가정하는 구현입니다.

## 4. Dijkstra보다 느린 이유 — O(V·E) vs O(E log V)

| 항목 | Dijkstra | Bellman-Ford |
|---|---|---|
| 방식 | "가장 가까운 노드"만 골라서 처리 (탐욕) | 모든 간선을 매번 전부 검사 (완전 탐색에 가까움) |
| 반복 횟수 | 정점마다 1번 확정 (`O(V)` 번의 `pop`) | 정점 수만큼(`O(V)`) 라운드 반복 |
| 라운드당 비용 | `O(log V)` (힙 연산) | `O(E)` (모든 간선 순회) |
| 총 시간복잡도 | `O(E log V)` | `O(V · E)` |

Dijkstra는 힙 덕분에 "다음에 확정할 노드"를 `O(log V)`만에 골라내지만, Bellman-Ford는 그런 지름길이 없어서 매 라운드마다 **모든 간선을 무조건 다 훑어야** 합니다. 대신 그 대가로 음수 가중치와 음수 사이클까지 다룰 수 있는 일반성을 얻습니다. 자세한 비교는 [`../dijkstra/README.md`의 5번 섹션](../dijkstra/README.md#5-dijkstra-vs-bellman-ford-비교)도 참고하세요.

## 5. 시간복잡도 / 공간복잡도

| 항목 | 복잡도 | 설명 |
|---|---|---|
| 시간복잡도 | `O(V · E)` | `V`번의 라운드 × 매 라운드 `E`개 간선 검사 |
| 공간복잡도 | `O(V)` | `distance`, `prev_index` 배열 |

## 6. 개념 ↔ 코드 대응표

| 개념 | 코드 위치 |
|---|---|
| 간선 목록에서 정점 개수 추론 | `vertex_set` / `vertex_count` (`bellman_ford.py:4-9`) |
| V번(=V-1번 이완 + 1번 검사) 반복 | `for loop_index in range(vertex_count):` (`bellman_ford.py:17`) |
| 모든 간선 이완(relaxation) | `for from_index, to_index, length in edge_list:` (`bellman_ford.py:18`) |
| 도달 불가능한 정점 건너뛰기 | `if distance[from_index] < INF ...` (`bellman_ford.py:19`) |
| 음수 사이클 탐지 | `if loop_index == vertex_count - 1: has_negative_cycle = True` (`bellman_ford.py:23-24`) |
| 경로 역추적 | `shortest_path()` (`bellman_ford.py:30`) |

## 7. 직접 실행해보기

`bellman_ford.py`에는 `if __name__ == '__main__':` 데모 블록이 없습니다. 아래처럼 직접 호출해볼 수 있습니다.

```bash
pytest tests/bellman_ford/test_bellman_ford.py -v
```

```bash
python3 -c "
from algorithm.bellman_ford.bellman_ford import bellman_ford, shortest_path

edges = [(0, 1, 4), (0, 2, 5), (1, 2, -3)]
distance, prev_index, has_negative_cycle = bellman_ford(edges, 0)
print('distance:', distance)
print('has_negative_cycle:', has_negative_cycle)
print('0 -> 2 경로:', shortest_path(prev_index, 2))
"
```

출력:

```
distance: [0, 4, 1]
has_negative_cycle: False
0 -> 2 경로: [0, 1, 2]
```

음수 사이클이 있는 그래프도 실행해볼 수 있습니다.

```bash
python3 -c "
from algorithm.bellman_ford.bellman_ford import bellman_ford
edges = [(0, 1, 1), (1, 2, -3), (2, 0, 1)]
print(bellman_ford(edges, 0))
"
```

---

[◀ 이전: Dijkstra 최단 경로](../dijkstra/README.md) | [다음: Floyd-Warshall 모든 쌍 최단 경로 ▶](../floyd_warshall/README.md)
