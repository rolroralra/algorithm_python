# AVL 트리 (AVL Tree)

> 구현: [`avl_tree.py`](./avl_tree.py) — `AVLTree` 클래스
> 이 문서를 읽기 전에 [`binary_search_tree.py`](./binary_search_tree.py)의 기본 BST(이진 탐색 트리) 개념을 먼저 알고 있다고 가정합니다.

## 1. 왜 AVL 트리가 필요한가?

일반 BST는 "왼쪽은 작은 값, 오른쪽은 큰 값"이라는 규칙만 지킬 뿐, 트리 모양이 어떻게 생기는지는 전혀 신경 쓰지 않습니다. 그래서 삽입 순서가 나쁘면 트리가 한쪽으로 완전히 치우쳐버립니다.

`binary_search_tree.py`의 `__main__` 데모에서 이미 이 문제를 확인했습니다. 정렬된 배열 `[1, 2, ..., 10]`을 순서대로 그대로 삽입하면:

```
sorted-order insert -> height: 10 (n=10)
```

즉, 노드 10개짜리 트리인데 높이가 10입니다. 사실상 연결 리스트(linked list)가 된 것이고, 탐색/삽입/삭제가 전부 `O(n)`이 되어버립니다 — BST를 쓰는 의미가 없어지는 셈입니다.

**AVL 트리는 이 문제를 "삽입/삭제할 때마다 스스로 모양을 고쳐서" 해결합니다.** 어떤 순서로 값을 넣더라도 항상 높이를 `O(log n)`으로 유지합니다. 1962년 Adelson-Velsky와 Landis가 고안한, 최초의 "자가 균형(self-balancing) BST"입니다 (이름 AVL은 두 사람 이름의 앞글자).

`avl_tree.py`의 데모에서 같은 정렬 배열을 넣어보면:

```
sorted-order insert -> height: 4 (n=10)
```

노드 10개에 높이 4 — `log2(10) ≈ 3.32`에 매우 가깝습니다.

## 2. 핵심 규칙: Balance Factor(균형 인수)

AVL 트리는 **모든 노드**에 대해 다음 규칙을 항상 만족해야 합니다:

> `왼쪽 서브트리의 높이 - 오른쪽 서브트리의 높이` 의 절댓값이 1 이하

이 값을 **balance factor(균형 인수)** 라고 부릅니다. 즉 각 노드에서 balance factor는 `-1`, `0`, `1` 중 하나여야만 "균형 잡힌" 상태입니다.

```
높이 계산: 노드가 없으면(None) 0, 리프 노드는 1, 그 외엔 1 + max(왼쪽 높이, 오른쪽 높이)

      5              balance factor(5) = height(left) - height(right)
     / \                                = 2 - 1 = 1   → OK (균형)
    3   8
   /
  1
```

만약 삽입이나 삭제 후 어떤 노드의 balance factor가 `2` 이상이거나 `-2` 이하가 되면, 그 지점에서 트리가 "기울었다"고 판단하고 **회전(rotation)** 으로 바로잡습니다.

**코드 연결**: `avl_tree.py`의 `_balance_factor()`가 이 값을 계산하고, `AVLNode.height` 필드가 각 노드의 높이를 저장합니다.

### 왜 매번 높이를 다시 계산하지 않고 `height` 필드에 저장해둘까?

`BinaryTree.height()`(`binary_tree.py`)는 트리 전체를 순회하면서 높이를 계산하므로 `O(n)`이 걸립니다. 그런데 AVL 트리는 삽입/삭제할 때마다 balance factor를 확인해야 하므로, 매번 `O(n)`으로 계산하면 전체 알고리즘이 `O(n log n)`으로 느려집니다.

그래서 `AVLNode`는 자기 자신의 높이를 `height` 필드에 미리 저장해두고(`_update_height()`), 자식의 높이가 필요할 때는 `_node_height()`로 그 필드를 `O(1)`에 그냥 읽기만 합니다. 이렇게 하면 균형을 맞추는 데 걸리는 시간이 `O(1)`이 되어, 삽입/삭제 전체가 `O(log n)`을 유지할 수 있습니다.

## 3. 회전(Rotation) — 기울어진 트리를 고치는 방법

균형이 깨졌을 때 고치는 경우는 정확히 4가지 패턴으로 나뉩니다. 아래 그림에서 `T1~T4`는 (있을 수도 없을 수도 있는) 서브트리를 뜻합니다.

### Case 1 — LL (왼쪽의 왼쪽이 무거움) → 오른쪽 회전 한 번

```
        z                                y
       / \                             /   \
      y   T4      right rotate(z)     x      z
     / \          ─────────────→    /  \    /  \
    x   T3                        T1   T2  T3   T4
   / \
  T1  T2
```

### Case 2 — RR (오른쪽의 오른쪽이 무거움) → 왼쪽 회전 한 번

```
    z                                  y
   /  \                              /   \
  T1   y        left rotate(z)      z      x
      /  \      ─────────────→     / \    / \
     T2   x                       T1  T2 T3  T4
         / \
        T3  T4
```

### Case 3 — LR (왼쪽의 오른쪽이 무거움) → 왼쪽 회전 후 오른쪽 회전

```
     z                       z                          x
    / \                     / \                        /  \
   y   T4   left rotate(y) x   T4   right rotate(z)    y    z
  / \       ────────────→ / \       ─────────────→   / \  / \
T1   x                   y   T3                     T1 T2 T3 T4
    / \                 / \
  T2   T3             T1   T2
```

### Case 4 — RL (오른쪽의 왼쪽이 무거움) → 오른쪽 회전 후 왼쪽 회전

Case 3을 좌우로 뒤집은 모양입니다 (대칭).

### 코드에서는 어떻게 판단할까?

`_rebalance()`(`avl_tree.py:119`)가 이 4가지를 다음과 같이 판단합니다:

```python
if balance_factor > 1:                       # 왼쪽이 무거움 (LL 또는 LR)
    if self._balance_factor(node.left) < 0:  # 왼쪽의 오른쪽이 무거우면 LR
        node.left = self._rotate_left(node.left)
    return self._rotate_right(node)          # LL은 바로, LR은 위에서 한 번 더 돌린 뒤 여기서

if balance_factor < -1:                      # 오른쪽이 무거움 (RR 또는 RL)
    if self._balance_factor(node.right) > 0: # 오른쪽의 왼쪽이 무거우면 RL
        node.right = self._rotate_right(node.right)
    return self._rotate_left(node)
```

- `balance_factor > 1` 이면서 자식(`node.left`)도 왼쪽으로 기울어져 있으면 → **LL**, 오른쪽 회전 한 번(단일 회전)
- `balance_factor > 1` 이면서 자식은 오른쪽으로 기울어져 있으면 → **LR**, 왼쪽 회전 후 오른쪽 회전(이중 회전)
- `RR`, `RL`은 좌우 대칭으로 동일한 논리

회전 자체는 `_rotate_left()` / `_rotate_right()`(`avl_tree.py:135-149`)가 담당하며, 포인터 3개를 바꿔치기하는 `O(1)` 연산입니다.

## 4. 삽입 과정 예시

`1, 2, 3`을 순서대로 삽입한다고 해봅시다 (전형적인 최악의 순서).

```
1 삽입:        1

2 삽입:        1
                \
                 2

3 삽입 직후:    1              balance_factor(1) = 0 - 2 = -2  → 불균형!
                \              node.right(2)의 balance_factor = 0 - 1 = -1 → RR case
                 2
                  \
                   3
```

`_insert()`는 재귀적으로 내려갔다가 올라오면서, **노드마다** `_rebalance()`를 호출합니다. 노드 `1`에서 불균형(`-2`)이 감지되고, 오른쪽 자식(`2`)도 오른쪽으로 기울어 있으므로 **RR case** → 왼쪽 회전 한 번으로 해결됩니다:

```
                 2
                / \
               1   3
```

`avl_tree.py`의 데모에서 `1~10`을 순서대로 넣었을 때 최종 트리 모양(`print_tree()` 출력)을 직접 실행해서 확인해볼 수 있습니다.

## 5. 삭제

삭제도 기본적인 BST 삭제(자식이 0/1개면 그대로 떼어내고, 2개면 오른쪽 서브트리의 최솟값으로 대체)를 먼저 수행한 뒤, **삭제 경로를 따라 올라오면서** 지나간 모든 조상 노드에 대해 `_rebalance()`를 호출합니다 (`avl_tree.py`의 `_delete()`, `_delete_min()`).

삽입과 다른 점 하나: 삽입은 회전이 최대 1~2번이면 전체 트리가 다시 균형 잡히지만, 삭제는 최악의 경우 루트까지 올라가며 `O(log n)`번 회전이 필요할 수 있습니다. (둘 다 여전히 `O(log n)` 안에 끝납니다.)

## 6. 시간복잡도

| 연산 | 일반 BST (최악) | AVL 트리 |
|---|---|---|
| 탐색 (search) | `O(n)` | `O(log n)` |
| 삽입 (insert) | `O(n)` | `O(log n)` |
| 삭제 (delete) | `O(n)` | `O(log n)` |
| 공간 | `O(n)` | `O(n)` (노드마다 `height` 정수 하나 추가) |

## 7. Red-Black 트리와 비교하면?

AVL 트리는 balance factor를 `±1`까지만 허용하는, **매우 엄격하게 균형 잡힌** 트리입니다. 그래서:
- 장점: 트리가 더 "낮고 납작"해서 탐색(search)이 Red-Black 트리보다 살짝 더 빠릅니다.
- 단점: 균형을 엄격히 유지하려다 보니 삽입/삭제 시 회전이 더 자주 필요할 수 있습니다.

반대로 Red-Black 트리는 균형 조건이 느슨한 대신 삽입/삭제가 평균적으로 더 저렴합니다. 자세한 설명은 [`RED_BLACK_TREE.md`](./RED_BLACK_TREE.md)를 참고하세요.

## 8. 개념 ↔ 코드 대응표

| 개념 | 코드 위치 |
|---|---|
| 균형 잡힌 이진 탐색 트리 클래스 | `AVLTree` (`avl_tree.py:18`) |
| 노드가 자기 높이를 기억 | `AVLNode.height` (`avl_tree.py:15`) |
| balance factor 계산 | `_balance_factor()` (`avl_tree.py:154`) |
| 균형 재조정 (회전 판단) | `_rebalance()` (`avl_tree.py:119`) |
| 단일/이중 회전 | `_rotate_left()`, `_rotate_right()` (`avl_tree.py:135`, `143`) |
| 삽입 | `insert()` → `_insert()` (`avl_tree.py:28`, `57`) |
| 삭제 | `delete()` → `_delete()` (`avl_tree.py:31`, `72`) |

## 9. 직접 실행해보기

```bash
python3 -m algorithm.binarysearch.avl_tree
```

`print_tree()` 출력으로 정렬된 배열을 넣어도 트리가 균형 잡힌 모양을 유지하는 걸 눈으로 확인할 수 있습니다. `binary_search_tree.py`의 worst-case 데모(높이 10)와 비교해보세요.
