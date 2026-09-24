# Floyd-Warshall 알고리즘 (모든 쌍 최단 경로, All-Pairs Shortest Path)

> 구현: [`floyd_warshall.py`](./floyd_warshall.py) — `floyd_warshall()`, `shortest_path()`
> 관련 테스트: [`test_floyd_warshall.py`](../../tests/floyd_warshall/test_floyd_warshall.py)
> 이 문서를 읽기 전에 [Dijkstra](../dijkstra/README.md), [Bellman-Ford](../bellman_ford/README.md) 문서를 먼저 읽는 것을 권장합니다.

## 1. 왜 Floyd-Warshall이 필요한가?

Dijkstra와 Bellman-Ford는 모두 **"한 출발점(single source)에서 다른 모든 정점까지"** 의 최단 거리를 구합니다. 그런데 "모든 도시 쌍 사이의 최단 거리표"처럼 **모든 정점 쌍(all-pairs)** 사이의 최단 거리가 필요하다면 어떻게 해야 할까요?

가장 단순한 방법은 모든 정점을 한 번씩 출발점으로 삼아 Dijkstra나 Bellman-Ford를 `V`번 돌리는 것입니다. 하지만 Floyd-Warshall은 이를 **동적 계획법(DP)** 으로 한 번에 풀어냅니다. 버스 노선도의 "모든 정류장 쌍 사이 최단 소요 시간표"나, 네트워크의 "모든 라우터 쌍 사이 지연 시간표"를 만들 때 유용합니다.

## 2. 핵심 아이디어: "경유지를 하나씩 허용해가며" 거리표 갱신하기

Floyd-Warshall의 핵심 질문은 이것입니다.

> **"정점 `i`에서 `j`로 갈 때, 정점 `k`를 경유지로 써도 될까?"**

정점을 `0`번부터 `V-1`번까지 순서대로 "경유지 후보"로 하나씩 허용해 나가면서, 그때마다 "그 경유지를 거치면 더 짧아지는 `(i, j)` 쌍이 있는지" 전부 확인합니다.

```
distance[i][j] = min(distance[i][j], distance[i][k] + distance[k][j])
```

**코드 연결**: `floyd_warshall.py:18-30`

```python
for k in range(vertex_count):                # k: 경유지로 새로 허용할 정점
    for i in range(vertex_count):
        if distance[i][k] == INF:
            continue
        for j in range(vertex_count):
            if distance[k][j] == INF:
                continue
            new_distance = distance[i][k] + distance[k][j]
            if new_distance < distance[i][j]:
                distance[i][j] = new_distance             # i -> k -> j 가 더 짧으면 갱신
                prev_index[i][j] = prev_index[k][j]
```

가장 바깥 반복문이 `k`(경유지)라는 점이 이 알고리즘의 핵심입니다. `k`가 `0`일 때는 "정점 0만 경유지로 써도 되는 세상"에서의 최단 거리표를 만들고, `k`가 `1`이 되면 "정점 0과 1을 둘 다 경유지로 써도 되는 세상"으로 넓어지는 식으로, **점점 더 많은 경유지를 허용하며 거리표를 완성**해 나갑니다.

## 3. DP 점화식을 표로 시각화하기

정점 3개, 간선 `0→1(3)`, `1→2(1)`, `0→2(10)`로 이루어진 그래프로 추적해봅니다.

```
        3          1
   0 ────────► 1 ────────► 2
    \                      ▲
     \__________10_________/
```

### 초기 상태 (경유지를 아직 하나도 허용하지 않음, 직접 간선만 반영)

| distance | 0 | 1 | 2 |
|---|---|---|---|
| **0** | 0 | 3 | 10 |
| **1** | INF | 0 | 1 |
| **2** | INF | INF | 0 |

### k=0 (정점 0을 경유지로 허용)

정점 0으로 들어오는 간선이 없으므로(`distance[i][0]`이 전부 `INF`) 변화 없음.

### k=1 (정점 1을 경유지로 허용)

`distance[0][1] + distance[1][2] = 3 + 1 = 4 < distance[0][2] (10)` → **갱신!**

| distance | 0 | 1 | 2 |
|---|---|---|---|
| **0** | 0 | 3 | **4** (10 → 4) |
| **1** | INF | 0 | 1 |
| **2** | INF | INF | 0 |

### k=2 (정점 2를 경유지로 허용)

정점 2에서 나가는 간선이 없으므로(`distance[2][j]`이 전부 `INF`) 변화 없음.

최종적으로 `0 → 2`의 최단 거리는 `4`(경로: `0 → 1 → 2`)로, 직접 간선(`10`)보다 훨씬 짧습니다. `floyd_warshall.py`로 직접 실행하면 이 결과를 그대로 확인할 수 있습니다(7번 섹션 참고).

## 4. 단일 출발점(Dijkstra·Bellman-Ford) vs 모든 쌍(Floyd-Warshall) 비교

| 구분 | Dijkstra / Bellman-Ford | Floyd-Warshall |
|---|---|---|
| 구하는 것 | 한 출발점 → 모든 정점 | 모든 정점 쌍 → 모든 정점 쌍 |
| 입력 형태 | 인접 리스트(`adj_list`) | 인접 행렬(`adj_matrix`) |
| 시간복잡도 | Dijkstra `O(E log V)`, Bellman-Ford `O(V·E)` | `O(V³)` |
| 음수 가중치 | Dijkstra 불가, Bellman-Ford 가능 | 가능 (단, 음수 사이클이 있으면 결과 무의미) |
| "모든 쌍"이 필요할 때 | 정점마다 알고리즘을 `V`번 반복해야 함 | 한 번의 실행으로 전부 계산 |
| 적합한 그래프 크기 | 정점 수가 많고 간선이 상대적으로 적은(sparse) 그래프 | 정점 수가 적당히 작은(보통 수백~수천 개 이하) 밀집(dense) 그래프 |

"딱 한 지점에서 출발"한다면 Dijkstra/Bellman-Ford가 훨씬 빠르고, "모든 지점 쌍의 거리표"가 필요하다면 `V`번 반복하는 것보다 Floyd-Warshall 한 번이 더 간단하고 (밀집 그래프에서는) 더 효율적입니다. 자세한 단일 출발점 비교는 [`../dijkstra/README.md`](../dijkstra/README.md#5-dijkstra-vs-bellman-ford-비교)를 참고하세요.

## 5. 시간복잡도 / 공간복잡도

| 항목 | 복잡도 | 설명 |
|---|---|---|
| 시간복잡도 | `O(V³)` | `k, i, j` 3중 반복문 |
| 공간복잡도 | `O(V²)` | `distance`, `prev_index` 두 개의 `V × V` 행렬 |

## 6. 개념 ↔ 코드 대응표

| 개념 | 코드 위치 |
|---|---|
| 거리 행렬 초기화 (자기 자신은 0, 직접 간선은 그 값) | `floyd_warshall.py:7-16` |
| 경유지 `k`를 하나씩 허용하며 갱신 (DP 점화식) | `for k in range(vertex_count):` (`floyd_warshall.py:18`) |
| `i -> k -> j`가 더 짧은지 비교 후 갱신 | `new_distance = distance[i][k] + distance[k][j]` (`floyd_warshall.py:27-30`) |
| 도달 불가능한 조합 건너뛰기 | `if distance[i][k] == INF: continue` (`floyd_warshall.py:20-21`, `24-25`) |
| 경로 역추적 (출발점별 `prev_index` 필요) | `shortest_path()` (`floyd_warshall.py:35`) |

## 7. 직접 실행해보기

`floyd_warshall.py`에는 `if __name__ == '__main__':` 데모 블록이 없습니다. 아래처럼 직접 호출해볼 수 있습니다.

```bash
pytest tests/floyd_warshall/test_floyd_warshall.py -v
```

```bash
python3 -c "
import sys
from algorithm.floyd_warshall.floyd_warshall import floyd_warshall, shortest_path

INF = sys.maxsize
matrix = [[INF] * 3 for _ in range(3)]
matrix[0][1] = 3
matrix[1][2] = 1
matrix[0][2] = 10

distance, prev_index = floyd_warshall(matrix)
for row in distance:
    print([x if x < INF else 'INF' for x in row])
print('0 -> 2 경로:', shortest_path(prev_index, 0, 2))
"
```

> 주의: 입력 `adj_matrix`의 대각선(`matrix[i][i]`)은 직접 `0`으로 채우지 말고 `INF`로 남겨두세요. `floyd_warshall()`이 내부적으로 `distance[i][i] = 0`을 채워주지만(`floyd_warshall.py:11`), 대각선에 미리 `0`(또는 `INF` 미만의 값)을 넣어두면 `prev_index[i][i]`에도 자기 자신이 기록되어(`floyd_warshall.py:16`) `shortest_path()`가 경로를 역추적할 때 `i -> i -> i -> ...`를 무한히 반복하는 문제가 생길 수 있습니다. `test_floyd_warshall.py`의 `build_matrix()` 헬퍼도 대각선을 건드리지 않는 이 안전한 패턴을 따릅니다.

출력:

```
[0, 3, 4]
['INF', 0, 1]
['INF', 'INF', 0]
0 -> 2 경로: [0, 1, 2]
```

위 3번 섹션의 DP 표 추적 결과(`distance[0][2]`가 `10`에서 `4`로 갱신됨)와 정확히 일치하는 것을 확인할 수 있습니다.

---

[◀ 이전: Bellman-Ford 최단 경로](../bellman_ford/README.md) | [다음: 위상 정렬 ▶](../topological_sort/README.md)
