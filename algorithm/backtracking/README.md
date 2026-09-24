# 백트래킹 (Backtracking)

> 구현: [`backtracking.py`](./backtracking.py) — `backtracking()`, `prunning()`
> 관련 테스트: [`tests/backtracking/test_backtracking.py`](../../tests/backtracking/test_backtracking.py)

## 1. 왜 이 알고리즘이 필요한가?

미로를 손전등 하나로 탐험한다고 상상해봅시다. 갈림길이 나올 때마다 한쪽 길로 들어가 보고, 막다른 길이면 **왔던 길로 되돌아와서(back-track)** 다른 길을 시도합니다. 이렇게 "일단 선택해보고, 안 되면 되돌아가서 다른 선택을 시도"하는 방식이 백트래킹입니다.

완전탐색(brute force)은 가능한 모든 경우의 수를 끝까지 다 만들어본 뒤에야 답을 고릅니다. 반면 백트래킹은 **한 걸음 나아갈 때마다 조건을 확인**해서, 가망이 없는 경로는 더 깊이 들어가지 않고 그 자리에서 포기합니다. 이 "가망 없는 가지를 미리 잘라내는 것"을 **가지치기(pruning)**라고 부릅니다. 가지치기를 잘 할수록, 완전탐색이었다면 오래 걸렸을 문제도 훨씬 빠르게 풀 수 있습니다.

이 파일의 `backtracking()`은 특정 퍼즐(N-Queen, 순열 등)에 종속되지 않은 **범용 뼈대(template)**입니다. 그래프(인접 리스트) 위에서 "방문 표시 → 자식 방문 → 방문 해제"라는 백트래킹의 핵심 패턴만 구현해두고, 실제 문제에 맞는 가지치기 조건은 `prunning()`을 채워 넣어 확장하도록 설계되어 있습니다.

## 2. 코드 흐름

```python
def backtracking(graph, is_visited, curr_index, *args):
    if prunning():                              # backtracking.py:2  — 가지치기: 더 갈 필요 없으면 즉시 반환
        return

    is_visited[curr_index] = True                # backtracking.py:5  — "선택": 현재 노드를 방문 처리

    for next_index in graph[curr_index]:          # backtracking.py:7  — 갈 수 있는 다음 노드들을 하나씩 시도
        if is_visited[next_index]:                 # backtracking.py:8  — 이미 방문했다면 건너뜀
            continue

        backtracking(graph, is_visited, next_index, *args)   # backtracking.py:11  — 재귀적으로 더 깊이 탐색

    is_visited[curr_index] = False                # backtracking.py:13 — "되돌리기": 방문 표시 해제(백트랙)


def prunning():
    return False    # backtracking.py:17 — 기본값: 가지치기 없음(항상 계속 진행)
```

이 구조는 백트래킹의 전형적인 3단계로 이루어져 있습니다.

1. **가지치기 확인** (`backtracking.py:2-3`) — 지금 상태가 가망이 없다면 아무것도 하지 않고 즉시 돌아갑니다.
2. **선택(선택지 적용)** (`backtracking.py:5`) — 현재 노드를 "방문했다"고 표시합니다.
3. **탐색 후 되돌리기** (`backtracking.py:7-13`) — 갈 수 있는 다음 노드들을 재귀적으로 전부 시도해본 뒤, 함수가 끝나기 직전에 **방문 표시를 다시 해제**합니다.

## 3. 단순 DFS와 무엇이 다른가?

그래프를 한 번만 훑어서 "도달 가능한 노드가 뭔지" 확인하는 일반적인 DFS(깊이 우선 탐색)라면, 방문 표시를 굳이 해제할 필요가 없습니다 — 한 번 방문했으면 그걸로 끝이니까요.

그런데 `backtracking()`은 함수가 끝나기 직전에 `is_visited[curr_index] = False`(`backtracking.py:13`)로 **방문 표시를 되돌립니다**. 이 한 줄이 바로 "백트래킹"을 "단순 DFS"와 구분 짓는 핵심입니다. 이 되돌리기 덕분에, 서로 다른 탐색 경로(가지)에서 **같은 노드를 다시 방문할 수 있습니다** — 이는 모든 경로/순열을 하나씩 나열해야 하는 문제(예: 모든 단순 경로 찾기, 순열 생성, N-Queen의 모든 배치 등)에서 꼭 필요한 동작입니다.

`test_unwinds_all_visit_marks_after_full_traversal`(`test_backtracking.py:9`)는 바로 이 성질을 검증합니다 — 전체 탐색이 끝난 뒤 `is_visited` 배열이 처음 상태(전부 `False`)로 완전히 복원되는지 확인합니다.

## 4. 탐색 트리로 보는 동작 — `graph = [[1, 2], [0, 3], [0], [1]]`

테스트에 쓰인 그래프(`test_backtracking.py:10`)는 다음과 같은 모양입니다 (무방향 그래프로 표현됨).

```
    0
   / \
  1   2
  |
  3
```

`backtracking(graph, is_visited, curr_index=0)`을 호출하면 다음 순서로 진행됩니다.

```
backtracking(0)
├─ is_visited[0] = True
├─ 이웃 1 (미방문) → backtracking(1)
│    ├─ is_visited[1] = True
│    ├─ 이웃 0 (이미 방문) → 건너뜀
│    ├─ 이웃 3 (미방문) → backtracking(3)
│    │    ├─ is_visited[3] = True
│    │    ├─ 이웃 1 (이미 방문) → 건너뜀
│    │    └─ is_visited[3] = False   (백트랙)
│    └─ is_visited[1] = False   (백트랙)
├─ 이웃 2 (미방문) → backtracking(2)
│    ├─ is_visited[2] = True
│    ├─ 이웃 0 (이미 방문) → 건너뜀
│    └─ is_visited[2] = False   (백트랙)
└─ is_visited[0] = False   (백트랙)

최종 결과: is_visited = [False, False, False, False]  (전부 원상 복구)
```

## 5. 가지치기(`prunning()`) — 지금은 빈 껍데기, 확장 지점

현재 `prunning()`(`backtracking.py:16-17`)은 인자도 받지 않고 항상 `False`만 반환합니다. 즉 지금 이 파일 상태로는 **가지치기가 실질적으로 동작하지 않으며**, 모든 도달 가능한 노드를 예외 없이 방문합니다. 이 함수는 구체적인 문제에 맞게 나중에 채워 넣도록 비워둔 "확장 지점(hook)"으로 볼 수 있습니다 — 예를 들어 "지금까지 고른 조합의 합이 목표값을 넘었다", "이미 정답보다 나쁜 상태다" 같은 조건을 넣으면 실제로 가지를 잘라낼 수 있습니다.

`test_pruning_stops_traversal_before_visiting`(`test_backtracking.py:40`)은 `monkeypatch`로 `prunning()`이 `True`를 반환하도록 바꿔서 이 동작을 검증합니다.

```python
monkeypatch.setattr(backtracking_module, "prunning", lambda: True)
graph = [[1, 2], [0], [0]]
is_visited = [False] * len(graph)

backtracking(graph, is_visited, 0)

assert is_visited == [False] * len(graph)   # 방문 표시조차 되지 않음
```

`prunning()`이 `True`를 반환하면 `backtracking.py:2-3`의 `if prunning(): return`에서 **`is_visited[curr_index] = True`(5번째 줄)에 도달하기도 전에** 함수가 종료됩니다. 즉 이 노드는 방문 표시조차 남기지 않고 통째로 건너뛰어집니다 — 완전탐색이었다면 이 노드와 그 아래로 이어지는 모든 경로를 하나하나 확인해야 했겠지만, 가지치기 한 번으로 그 서브트리 전체를 통째로 잘라낸 것입니다.

## 6. 완전탐색 대비 백트래킹이 효율적인 이유

| | 완전탐색 (Brute Force) | 백트래킹 (Backtracking) |
|---|---|---|
| 진행 방식 | 가능한 모든 조합/경로를 끝까지 만들어본 뒤 검사 | 한 단계씩 나아가며 그때그때 조건을 확인 |
| 가망 없는 경로 처리 | 끝까지 만든 다음에야 버림 | `prunning()`으로 더 들어가기 **전에** 미리 버림 |
| 최악의 경우 시간복잡도 | 조합의 개수에 비례 (그래프 탐색이면 `O(V+E)`류, 순열/조합이면 `O(n!)`, `O(2^n)` 등 문제에 따라 다름) | 이론상 최악은 완전탐색과 같지만, 가지치기가 유효할수록 실제로 탐색하는 경우의 수가 크게 줄어듦 |

가지치기가 하나도 없다면(`prunning()`이 항상 `False`) 백트래킹은 사실상 완전탐색(모든 도달 가능 경로 탐색)과 동일한 일을 합니다. 백트래킹의 가치는 **얼마나 똑똑하게 `prunning()` 조건을 세우느냐**에 달려 있습니다 — 이 파일은 그 틀만 제공하고, 실제 문제(N-Queen, 순열, 부분집합 합 등)에 맞는 조건은 사용하는 쪽에서 채워 넣도록 설계되어 있습니다.

## 7. 시간복잡도 / 공간복잡도

| 항목 | 복잡도 |
|---|---|
| 시간복잡도 (가지치기 없이 전체 탐색 시) | `O(V + E)` (그래프의 모든 정점/간선을 한 번씩) |
| 공간복잡도 | `O(V)` (재귀 호출 스택 + `is_visited` 배열) |
| 가지치기가 유효할 때 | 실제 방문하는 노드 수가 줄어들어 위 상한보다 훨씬 빨라질 수 있음 (문제와 `prunning()` 구현에 따라 다름) |

## 8. 개념 ↔ 코드 대응표

| 개념 | 코드 위치 |
|---|---|
| 가지치기(더 볼 필요 없으면 즉시 반환) | `if prunning(): return` (`backtracking.py:2-3`) |
| 선택(현재 노드를 "썼다"고 표시) | `is_visited[curr_index] = True` (`backtracking.py:5`) |
| 다음 선택지 탐색 (미방문 이웃만) | `for next_index in graph[curr_index]: if is_visited[...]: continue` (`backtracking.py:7-9`) |
| 재귀적으로 더 깊이 탐색 | `backtracking(graph, is_visited, next_index, *args)` (`backtracking.py:11`) |
| 되돌리기(백트랙) — 단순 DFS와의 결정적 차이 | `is_visited[curr_index] = False` (`backtracking.py:13`) |
| 가지치기 조건의 확장 지점(현재는 비어있음) | `prunning()` (`backtracking.py:16-17`) |
| 문제별 추가 상태 전달 통로 | `*args` (`backtracking.py:1`, `11`) |

## 9. 직접 실행해보기

이 파일에는 `if __name__ == '__main__':` 데모 블록이 없으므로, 함수를 직접 호출해서 동작을 확인합니다.

```bash
python3 -c "
from algorithm.backtracking.backtracking import backtracking

graph = [[1, 2], [0, 3], [0], [1]]
is_visited = [False] * len(graph)
backtracking(graph, is_visited, 0)
print('탐색 후 방문 표시:', is_visited)  # 전부 False로 복원되어야 함
"
```

`prunning()`을 몽키패치해서 가지치기가 실제로 탐색을 멈추게 하는 모습은 테스트 코드에서 직접 확인할 수 있습니다.

```bash
pytest tests/backtracking/test_backtracking.py -v
```

---

이전 문서: [← 배낭 문제 (0/1 Knapsack)](../knapsack/README.md) | 다음 문서 없음 (알고리즘 시리즈의 마지막 문서입니다)
