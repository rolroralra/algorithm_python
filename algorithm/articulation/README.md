# 단절점과 단절선 (Articulation Points & Bridges)

> 구현: [`articulation_point.py`](./articulation_point.py) — `articulation_points()`, [`articulation_edge.py`](./articulation_edge.py) — `articulation_edges()`

## 1. 왜 필요한가? — 그래프의 "취약점" 찾기

네트워크(도로망, 통신망, 전력망, 조직도)를 그래프로 표현했을 때, 이런 질문을 던질 수 있습니다.

- "이 라우터(정점) 하나가 고장 나면, 네트워크의 일부가 서로 통신할 수 없게 되는가?"
- "이 도로(간선) 하나가 끊기면, 두 마을이 서로 갈 수 없게 되는가?"

이렇게 **제거했을 때 그래프가 더 많은 연결 요소(connected component)로 쪼개지는 지점**을 찾는 문제입니다. 이런 지점은 네트워크 설계에서 "이중화가 필요한 취약 구간"을 찾는 데 직접적으로 쓰입니다.

## 2. 단절점 vs 단절선 — 차이는 "무엇을 제거하는가"

| | 단절점 (Articulation Point / Cut Vertex) | 단절선 (Articulation Edge / Bridge) |
|---|---|---|
| 제거 대상 | 정점(vertex) 하나 | 간선(edge) 하나 |
| 판정 기준 | 그 정점을 제거하면 연결 요소 수가 늘어난다 | 그 간선을 제거하면 연결 요소 수가 늘어난다 |
| 구현 | `articulation_points()` (`articulation_point.py`) | `articulation_edges()` (`articulation_edge.py`) |

```
    0---1---3---4          0을 지우면: 1,2,3,4는 여전히 서로 연결됨 → 0은 단절점 아님
     \ /                    1을 지우면: {0,2} 와 {3,4}로 쪼개짐      → 1은 단절점
      2                     3을 지우면: {0,1,2} 와 {4}로 쪼개짐      → 3은 단절점

                            간선(1,3)을 지우면: {0,1,2} 와 {3,4}로 쪼개짐 → (1,3)은 단절선(다리)
                            간선(3,4)를 지우면: {0,1,2,3} 와 {4}로 쪼개짐 → (3,4)는 단절선(다리)
                            간선(0,1)을 지우면: 0-2-1로 여전히 연결됨    → (0,1)은 단절선 아님 (삼각형의 일부)
```

이 예시 그래프(삼각형 `0-1-2` + 다리 `1-3` + 펜던트 `3-4`)는 두 문서 전체에서 공통 예시로 사용합니다.

## 3. 공통 원리: DFS + discovery time + low-link

두 알고리즘 모두 그래프를 한 번의 DFS(깊이 우선 탐색)로 순회하면서 `O(V + E)`에 답을 구합니다. 공통으로 쓰이는 두 가지 값:

- **discovery time (방문 순서)**: 각 정점을 DFS로 처음 방문한 순서. 코드에서는 `visit[]` 배열.
- **low-link 값**: 그 정점의 DFS 서브트리에서, **역방향 간선(back edge)을 통해 도달할 수 있는 가장 이른(가장 작은) discovery time**. "이 서브트리가 트리 간선을 거치지 않고 얼마나 위쪽 조상까지 닿을 수 있는가"를 나타냅니다.

이 값들을 어떻게 비교하느냐에 따라 단절점과 단절선의 판정 조건이 미묘하게(하지만 중요하게) 달라집니다. 자세한 내용은 아래 두 문서에서 다룹니다.

- [ARTICULATION_POINT.md](./ARTICULATION_POINT.md) — 단절점을 찾는 원리, 루트 노드의 특수 케이스
- [ARTICULATION_EDGE.md](./ARTICULATION_EDGE.md) — 단절선을 찾는 원리, 단절점 판정과의 결정적 차이

## 4. 시간복잡도 요약

| 알고리즘 | 시간복잡도 | 공간복잡도 |
|---|---|---|
| `articulation_points()` | `O(V + E)` | `O(V)` |
| `articulation_edges()` | `O(V + E)` | `O(V)` |

---

이전 문서: [← 최소 공통 조상 (LCA)](../lca/README.md)
다음 문서: [단절점 (Articulation Point) →](./ARTICULATION_POINT.md)
