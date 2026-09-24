# 레드-블랙 트리 (Red-Black Tree)

> 구현: [`red_black_tree.py`](./red_black_tree.py) — `RedBlackTree` 클래스 (Left-Leaning Red-Black Tree, Sedgewick & Wayne 방식)
> 이 문서를 읽기 전에 [`AVL_TREE.md`](./AVL_TREE.md)를 먼저 읽어보는 걸 권장합니다. "왜 자가 균형 트리가 필요한가"는 두 문서가 동일하기 때문입니다.

## 1. Red-Black 트리는 AVL 트리와 뭐가 다른가?

[AVL 트리](./AVL_TREE.md)는 모든 노드의 balance factor를 `±1` 이내로 **엄격하게** 유지합니다. Red-Black 트리는 조금 다른 전략을 씁니다 — 각 노드에 **색(RED 또는 BLACK)** 을 하나씩 붙이고, "색깔에 대한 규칙"만 지키면 높이가 자동으로 `O(log n)` 안에 들어오도록 만듭니다. AVL보다 균형 조건이 느슨한 대신, 삽입/삭제 시 트리 구조를 덜 건드려도 됩니다.

그래서 실무에서 굉장히 많이 쓰입니다: C++ STL의 `std::map`/`std::set`, Java의 `TreeMap`/`TreeSet`, Linux 커널의 스케줄러 등이 전부 Red-Black 트리 계열입니다.

## 2. Red-Black 트리의 규칙 (속성)

1. 모든 노드는 **RED** 아니면 **BLACK**이다.
2. 루트(root)는 항상 **BLACK**이다.
3. 존재하지 않는 자식(`None`)은 **BLACK**이라고 간주한다.
4. **RED 노드의 자식은 반드시 BLACK이다.** (RED가 두 번 연달아 나올 수 없다 — "no red-red")
5. 임의의 노드에서 그 아래로 뻗어나가는 모든 경로는, 지나가는 **BLACK 노드의 개수가 전부 동일**하다. 이 개수를 **black-height(블랙 높이)** 라고 부른다.

이 5가지를 지키면 **가장 긴 경로가 가장 짧은 경로의 2배를 넘지 못한다**는 게 수학적으로 증명되어 있습니다 (규칙 4 때문에 RED는 절대 연속으로 못 나오니, 최악의 경우도 BLACK-RED-BLACK-RED... 로 기존 경로의 최대 2배까지만 늘어날 수 있음). 그 결과 트리의 높이는 항상 `O(log n)`으로 묶입니다.

```
✅ 올바른 예                       ❌ 규칙 4 위반 (RED 연속)
      10(B)                              10(B)
     /    \                             /    \
   5(R)   15(R)                       5(R)   15(B)
   /                                  /
  1(B)                              1(R)   ← RED의 자식이 RED! 위반
```

## 3. 직관적으로 이해하기: "2-3 트리"로 생각하기

Red-Black 트리를 처음 볼 때 가장 헷갈리는 부분이 "색깔을 왜 이렇게 바꾸는지"인데, 다음과 같이 생각하면 훨씬 쉬워집니다.

> **BLACK 노드와 그 노드에 매달린 RED 자식(들)을 "하나의 뭉치"로 묶어서 생각하자.**

- BLACK 노드 혼자 → 값 1개짜리 뭉치 (2-node)
- BLACK 노드 + RED 자식 1개 → 값 2개짜리 뭉치 (3-node)
- BLACK 노드 + RED 자식 2개 → 값 3개짜리 뭉치 (4-node, 일시적으로만 허용)

```
BLACK 노드 하나           BLACK + RED 자식 하나         BLACK + RED 자식 둘
     5(B)                     5(B)                          5(B)
                              /                             /   \
                            3(R)                          3(R)  8(R)

    [ 5 ]                  [3, 5]                        [3, 5, 8]
   (2-node)               (3-node)                       (4-node, 임시 상태)
```

이렇게 보면 Red-Black 트리는 사실 **"2-3 트리"(한 뭉치에 값을 1개 또는 2개까지 담는 트리)를 이진 트리로 표현한 것**입니다. 삽입할 때 뭉치가 꽉 차서 4-node가 되면, 가운데 값을 위로 올려보내고 나머지 둘로 쪼개는데 — 이 "쪼개기"가 바로 코드의 `_flip_colors()`입니다.

## 4. 이 구현의 특징: Left-Leaning (왼쪽으로 기울인 RED 링크)

일반적인 Red-Black 트리는 RED 링크가 왼쪽/오른쪽 어디로든 붙을 수 있어서, 처리해야 할 경우의 수가 많고 구현이 꽤 복잡합니다.

`red_black_tree.py`가 구현한 **Left-Leaning Red-Black Tree(LLRB)** 는 Robert Sedgewick이 고안한 변형으로, 규칙을 하나 더 추가합니다:

> **RED 링크는 항상 왼쪽 자식으로만 향한다.**

이 제약 덕분에 3-node(값 2개짜리 뭉치)를 표현하는 방법이 단 하나로 정해지고, 삽입/삭제 로직이 재귀 함수 몇 개로 깔끔하게 정리됩니다. `_balance()`의 첫 줄이 바로 이 규칙을 강제하는 부분입니다:

```python
def _balance(self, node):
    if self._is_red(node.right) and not self._is_red(node.left):
        node = self._rotate_left(node)   # RED가 오른쪽에 붙어있으면 왼쪽으로 돌려서 고침
    ...
```

## 5. 삽입: 회전(rotation)과 색 뒤집기(color flip)

새 노드는 항상 **RED**로 삽입합니다 (`RBNode.__init__`의 기본값, `red_black_tree.py:14`). 방금 배운 "뭉치" 비유로 보면, 기존 뭉치에 값 하나를 끼워 넣는 것과 같습니다. 그런데 이렇게 끼워 넣다 보면 규칙 4(RED 연속 금지)가 깨지는 3가지 상황이 생길 수 있고, `_balance()`가 이를 순서대로 고칩니다.

```python
def _balance(self, node):
    if self._is_red(node.right) and not self._is_red(node.left):
        node = self._rotate_left(node)
    if self._is_red(node.left) and self._is_red(node.left.left):
        node = self._rotate_right(node)
    if self._is_red(node.left) and self._is_red(node.right):
        self._flip_colors(node)
    return node
```

### ① RED가 오른쪽에 붙음 → 왼쪽 회전

```
    5(B)                    8(B)
       \        left           /
       8(R)   rotate(5)      5(R)
      ─────────────────→
```

### ② RED가 왼쪽-왼쪽으로 연속됨 → 오른쪽 회전

```
        8(B)                  5(R)
       /          right      /    \
     5(R)       rotate(8)   3(B)  8(B)
    /           ────────→
  3(R)
```

### ③ 양쪽 자식이 둘 다 RED → 색 뒤집기 (color flip)

일시적으로 생긴 4-node(값 3개짜리 뭉치)를 둘로 쪼개서 가운데 값을 위로 올려 보내는 것과 같습니다. 부모는 RED가 되어 "한 단계 위 뭉치에 합류"를 시도합니다.

```
       5(B)                    5(R)   ← 부모가 RED가 되어 한 단계 위로 전파
      /    \      flip        /    \
    3(R)   8(R)  colors     3(B)   8(B)
```

이 세 규칙을 삽입 경로를 따라 **아래에서 위로** 올라가며 반복 적용하면, 최종적으로 루트까지 정리가 끝나고 `insert()`(`red_black_tree.py:33`)의 마지막 줄에서 루트를 다시 BLACK으로 강제합니다 (규칙 2: 루트는 항상 BLACK).

## 6. 삭제: `move_red_left` / `move_red_right`

삭제는 Red-Black 트리에서 가장 까다로운 부분입니다. 핵심 아이디어만 이해하면 충분합니다:

- BLACK 노드를 그냥 제거해버리면 그 경로의 black-height가 줄어들어서 규칙 5가 깨집니다.
- 그래서 삭제하기 **전에**, 지나가는 경로에 있는 노드가 항상 "RED이거나, 최소 3-node 이상"이 되도록 미리 만들어 둡니다 (2-3 트리 비유로: 값 1개짜리 뭉치를 그냥 지나가면 위험하니, 지나가기 전에 옆 뭉치에서 값을 하나 빌려오거나 합쳐버림).
- 이 "미리 여유를 만드는" 작업이 `_move_red_left()` / `_move_red_right()`(`red_black_tree.py:172`, `180`)이고, 내려갈 때마다 이걸 호출한 뒤 `_balance()`로 마무리합니다.

```python
def _delete(self, node, value):
    if self.comp(value, node.value) < 0:
        if not self._is_red(node.left) and not self._is_red(node.left.left):
            node = self._move_red_left(node)   # 왼쪽으로 내려가기 전에 여유 확보
        node.left = self._delete(node.left, value)
    else:
        ...
    return self._balance(node)
```

이 부분은 처음 볼 때 완벽히 이해하지 못해도 괜찮습니다 — Red-Black 트리 삭제는 원 저자(Sedgewick)도 "구현하기 까다로운 부분"이라고 인정한 영역입니다. **"삭제 전에 지나갈 경로를 미리 튼튼하게 만들어 둔다"** 는 아이디어만 기억해두면 충분합니다.

## 7. 시간복잡도

| 연산 | 일반 BST (최악) | Red-Black 트리 |
|---|---|---|
| 탐색 (search) | `O(n)` | `O(log n)` |
| 삽입 (insert) | `O(n)` | `O(log n)` |
| 삭제 (delete) | `O(n)` | `O(log n)` |
| 공간 | `O(n)` | `O(n)` (노드마다 색 1비트 추가) |

## 8. AVL 트리와 비교

| | AVL 트리 | Red-Black 트리 |
|---|---|---|
| 균형 기준 | balance factor `±1` (엄격) | black-height 규칙 (느슨) |
| 트리 높이 | 더 낮고 납작함 | AVL보다 약간 더 높을 수 있음 |
| 탐색(search) | 약간 더 빠름 | 약간 더 느림 |
| 삽입/삭제 | 회전이 더 잦을 수 있음 | 회전이 평균적으로 더 적음 |
| 실무 사용처 | 읽기(조회)가 압도적으로 많은 경우 | C++ `map`/Java `TreeMap` 등 범용 |

둘 다 최악의 경우에도 `O(log n)`을 보장한다는 점은 동일합니다. "얼마나 엄격하게 균형을 맞추느냐"의 트레이드오프 차이입니다.

## 9. 개념 ↔ 코드 대응표

| 개념 | 코드 위치 |
|---|---|
| 균형 잡힌 이진 탐색 트리 클래스 | `RedBlackTree` (`red_black_tree.py:21`) |
| 노드 색 | `RBNode.color` (`red_black_tree.py:18`), `RED`/`BLACK` 상수 (`red_black_tree.py:9-10`) |
| RED 판별 | `_is_red()` (`red_black_tree.py:136`) |
| 왼쪽으로 기울이기 + 색 뒤집기 정리 | `_balance()` (`red_black_tree.py:162`) |
| 4-node 쪼개기 (색 뒤집기) | `_flip_colors()` (`red_black_tree.py:156`) |
| 회전 | `_rotate_left()`, `_rotate_right()` (`red_black_tree.py:140`, `148`) |
| 삭제 전 경로 여유 확보 | `_move_red_left()`, `_move_red_right()` (`red_black_tree.py:172`, `180`) |
| 삽입 | `insert()` → `_insert()` (`red_black_tree.py:33`, `73`) |
| 삭제 | `delete()` → `_delete()` (`red_black_tree.py:37`, `88`) |

## 10. 직접 실행해보기

```bash
python3 -m algorithm.binarysearch.red_black_tree
```

`print_tree()` 출력으로는 색 정보가 보이지 않으니, 궁금하면 `RBNode.color`를 직접 찍어보며 규칙 4/5가 항상 지켜지는지 확인해봐도 좋습니다. `binary_search_tree.py`의 worst-case 데모(높이 10)와 비교하면, 정렬된 배열을 그대로 넣어도 트리가 낮게 유지되는 걸 확인할 수 있습니다.

---

[◀ 이전: AVL 트리](./AVL_TREE.md) | [인덱스로 돌아가기 ▶](./README.md)
