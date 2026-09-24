# 이진 탐색 트리 (Binary Search Tree)

> 구현: [`binary_search_tree.py`](./binary_search_tree.py) — `BSTNode`, `BinarySearchTree` 클래스
> [`AVL_TREE.md`](./AVL_TREE.md), [`RED_BLACK_TREE.md`](./RED_BLACK_TREE.md)가 "균형을 어떻게 유지하는가"를 다룬다면, 이 문서는 그 두 트리가 공통으로 딛고 서 있는 **기본 BST의 삽입/삭제, 그리고 그 둘을 떠받치는 `_transplant`** 를 다룹니다.

## 1. 노드 구조: `BSTNode`

```python
class BSTNode(Generic[T]):
    def __init__(self, value: T):
        self.value = value
        self.left: BSTNode[T] | None = None
        self.right: BSTNode[T] | None = None
        self.parent: BSTNode[T] | None = None
```

`AVLNode`/`RBNode`와 달리 `BSTNode`는 **`parent` 포인터**를 갖습니다. 자식만 보면 트리를 위에서 아래로만 훑을 수 있지만, 삭제 로직(특히 `_transplant`)은 "이 노드가 부모의 왼쪽 자식인지 오른쪽 자식인지"를 계속 물어봐야 하므로 부모 포인터가 필요합니다.

이 관계를 매번 손으로 묻지 않도록, `BSTNode`에 질의용 메서드를 몇 개 붙여뒀습니다.

| 메서드 | 의미 |
|---|---|
| `is_leaf()` | 자식이 하나도 없는가 |
| `is_internal()` | `is_leaf()`의 반대 |
| `is_root()` | `parent is None`인가 |
| `is_left_child()` / `is_right_child()` | 내가 부모의 왼쪽/오른쪽 자식인가 (`self is self.parent.left`) |
| `has_left_child()` / `has_right_child()` | 왼쪽/오른쪽 자식이 있는가 |

그리고 자식을 갈아 끼울 때 `parent` 동기화를 깜빡하는 실수를 막기 위한 헬퍼도 있습니다:

```python
def set_left(self, child: 'BSTNode[T] | None') -> None:
    self.left = child
    if child is not None:
        child.parent = self

def set_right(self, child: 'BSTNode[T] | None') -> None:
    self.right = child
    if child is not None:
        child.parent = self
```

`node.left = child` 처럼 필드를 직접 대입하면 `child.parent`를 갱신하는 걸 잊기 쉽습니다. `set_left`/`set_right`는 "자식 연결"과 "부모 역방향 연결"을 항상 한 쌍으로 묶어서, 이후 나올 삽입·삭제·`_transplant` 코드 전체가 이 메서드 하나에 의존하게 만듭니다.

## 2. 재귀 vs 루프: 왜 두 가지 경로가 있는가?

이 구현은 삽입/삭제/탐색 모두 **같은 연산을 재귀와 루프 두 가지로 구현**해두고, 트리 크기에 따라 골라 씁니다.

```python
def _insert(self, value: T):
    if self.size() < 1000:
        self.root = self._insert_by_recursive(self.root, value)
    else:
        self._insert_by_loop(value)
```

- 노드가 적을 때(`< 1000`)는 재귀가 더 읽기 쉬우니 재귀를 씁니다.
- 노드가 많을 때는 BST가 한쪽으로 치우치면(스큐드 트리) 재귀 깊이가 노드 수만큼 깊어질 수 있어 파이썬의 재귀 한도(`RecursionError`)에 걸릴 위험이 있습니다. 그래서 루프 버전으로 전환합니다.

`_delete`, `_find`도 동일한 패턴입니다. 이 문서에서는 두 경로를 각각 설명하되, **핵심 로직(특히 삭제)은 결국 같은 헬퍼(`_delete_node`, `_transplant`)로 수렴**한다는 점이 포인트입니다.

## 3. 삽입 (Insert)

### 3-1. 재귀 버전 — `_insert_by_recursive`

```python
def _insert_by_recursive(self, node: BSTNode[T] | None, value: T) -> BSTNode[T]:
    if node is None:
        self._increase_size()
        return BSTNode(value)

    comparison = self.comp(value, node.value)
    if comparison < 0:
        node.set_left(self._insert_by_recursive(node.left, value))
    elif comparison > 0:
        node.set_right(self._insert_by_recursive(node.right, value))

    return node
```

가장 교과서적인 형태입니다. `value`가 현재 노드보다 작으면 왼쪽으로, 크면 오른쪽으로 내려가다가 `None`(빈 자리)을 만나면 그 자리에 새 노드를 만들어 반환합니다. 반환값을 `node.set_left(...)`/`node.set_right(...)`로 다시 연결하면서 올라오므로, 재귀가 끝나면 트리 전체가 자연스럽게 다시 이어집니다.

### 3-2. 루프 버전 — 탐색과 연결의 분리

루프 버전은 "삽입할 위치(부모 노드)를 찾는 일"과 "그 부모에 실제로 노드를 붙이는 일"을 두 메서드로 나눴습니다.

```python
def find_leaf_node_having_value(self, value: T) -> tuple[BSTNode[T] | None, int]:
    parent, current = None, self.root
    comparison = 0
    while current is not None:
        comparison = self.comp(value, current.value)
        if comparison == 0:
            return current, 0          # 중복: 같은 값의 기존 노드를 그대로 반환

        parent = current
        current = current.left if comparison < 0 else current.right

    return parent, comparison
```

`self.root`부터 시작해 `current`가 `None`이 될 때까지 내려가면서 `parent`를 한 칸씩 따라갑니다. 루프가 끝나면 `parent`는 "새 값이 자식으로 붙을 자리"이고, `comparison`은 그 부모의 어느 쪽(왼쪽/오른쪽)에 붙어야 하는지를 말해줍니다.

```python
def _insert_node_into_parent_node(self, parent: BSTNode[T] | None, node: BSTNode[T] | None) -> None:
    if parent is None or node is None:
        return

    comparison = self.comp(node.value, parent.value)
    if comparison < 0:
        parent.set_left(node)
    elif comparison > 0:
        parent.set_right(node)
    else:
        return   # 중복 값, 삽입하지 않음

    self._increase_size()
```

`find_leaf_node_having_value`가 찾아준 자리에 `set_left`/`set_right`로 실제로 꽂아 넣고 크기를 늘립니다. 중복 값이면 아무것도 하지 않습니다.

### 3-3. 삽입 예시

```
5, 3, 8 삽입:
        5
       / \
      3   8

4 삽입 (5보다 작고, 3보다 큼):
        5
       / \
      3   8
       \
        4
```

## 4. `_transplant` — 삭제를 지탱하는 핵심 연산

삭제를 이해하기 전에 `_transplant`부터 봐야 합니다. 삭제의 모든 경우(자식 0개/1개/2개)가 결국 이 연산 하나로 표현되기 때문입니다. (CLRS "Introduction to Algorithms"의 `TRANSPLANT`를 그대로 옮긴 것입니다.)

### 4-1. 개념

> **`target`이 트리에서 차지하고 있던 "자리"를, `replacement`(가 루트인 서브트리)로 갈아 끼운다.**

여기서 "자리"는 `target.parent`가 `target`을 가리키던 그 링크 하나를 말합니다. `target` 자신의 `left`/`right`는 건드리지 않습니다 — 이 연산은 순수하게 "부모 쪽 링크 하나를 바꿔 끼우는" 것만 책임집니다.

```
     P                         P
    /                         /
  target      _transplant(target, replacement)      replacement
  /   \       ──────────────────────────────►
 A     B                                          (target.left, target.right는 그대로 유지되지만
                                                    더 이상 트리에서 참조되지 않음)
```

### 4-2. 코드

```python
def _transplant(self, target: BSTNode[T] | None, replacement: BSTNode[T] | None) -> None:
    if target is None:
        return

    if target.is_root():
        self.root = replacement
        if replacement is not None:
            replacement.parent = None
    elif target.is_left_child():
        target.parent.set_left(replacement)
    else:
        target.parent.set_right(replacement)
```

경우는 딱 세 가지뿐입니다:

1. **`target`이 루트다** → `self.root`를 직접 `replacement`로 바꾼다.
2. **`target`이 부모의 왼쪽 자식이다** → `target.parent.set_left(replacement)`
3. **`target`이 부모의 오른쪽 자식이다** → `target.parent.set_right(replacement)`

`set_left`/`set_right`를 쓰기 때문에 `replacement`가 `None`이 아니면 `replacement.parent`도 자동으로 갱신됩니다. `replacement`가 `None`이어도(자식이 없는 자리로 대체) 안전합니다.

**주의**: `_transplant`는 `replacement`를 그 자리에 "꽂기만" 합니다. `replacement`가 원래 갖고 있던 `left`/`right` 서브트리는 손대지 않으므로, `replacement`가 원래 다른 자리에 있던 노드라면(삭제의 2-자식 케이스처럼) 호출하는 쪽에서 그 서브트리를 어떻게 처리할지 직접 책임져야 합니다. 아래 5장에서 바로 이 상황이 나옵니다.

## 5. 삭제 (Delete)

### 5-1. 노드 찾기 — 재귀 vs 루프

```python
def _delete_by_recursive(self, node: BSTNode[T] | None, value: T) -> None:
    if node is None:
        return

    comparison = self.comp(value, node.value)
    if comparison < 0:
        self._delete_by_recursive(node.left, value)
    elif comparison > 0:
        self._delete_by_recursive(node.right, value)
    else:
        self._delete_node(node)
```

```python
def _delete_by_loop(self, value: T) -> None:
    current = self.root
    while current is not None:
        comparison = self.comp(value, current.value)
        if comparison < 0:
            current = current.left
        elif comparison > 0:
            current = current.right
        else:
            break

    if current is None:
        return

    self._delete_node(current)
```

두 버전 모두 "값으로 노드를 찾는" 역할만 하고, **찾은 뒤에는 똑같이 `_delete_node(node)`를 호출**합니다. `_transplant`가 `.parent`를 통해 부모 쪽 링크를 직접 고쳐주기 때문에, 재귀 버전도 (옛날 BST 구현들이 흔히 하듯) "반환값을 받아서 `node.left = ...`로 재할당"할 필요가 없습니다 — 재귀는 순수하게 탐색만 담당합니다.

### 5-2. `_delete_node` — 세 가지 케이스

```python
def _delete_node(self, node: BSTNode[T]):
    if node.left is None:
        self._transplant(node, node.right)
    elif node.right is None:
        self._transplant(node, node.left)
    else:
        next_node = self.successor(node)
        if next_node is not node.right:
            self._transplant(next_node, next_node.right)
            next_node.set_right(node.right)

        self._transplant(node, next_node)
        next_node.set_left(node.left)

    self._decrease_size()
```

#### 케이스 1 — 왼쪽 자식이 없다

`node`의 자리를 오른쪽 자식으로 그대로 갈아 끼우면 끝입니다.

```
   P                    P
    \                    \
    node      ──►        node.right
      \
       node.right
```
`self._transplant(node, node.right)` 한 줄.

#### 케이스 2 — 오른쪽 자식이 없다

대칭입니다. `self._transplant(node, node.left)`.

#### 케이스 3 — 자식이 둘 다 있다

가장 까다로운 경우입니다. 전략은: **`node`의 오른쪽 서브트리에서 가장 작은 값(= in-order successor)을 찾아, 그 노드를 `node`의 자리로 옮긴다.**

```python
next_node = self.successor(node)
```

여기서 `node.right`가 `None`이 아님이 보장되므로(케이스 1/2를 이미 걸렀으니까), `successor(node)`는 내부적으로 `find_min_node(node.right)`와 같습니다 — `node.right` 서브트리에서 가장 왼쪽(가장 작은) 노드입니다.

이제 `next_node`가 `node.right` 자신인지 아닌지에 따라 두 갈래로 나뉩니다.

**(a) `next_node`가 `node.right` 그 자체인 경우** — `node.right` 서브트리 자체가 왼쪽 자식이 없어서, 그 루트가 곧 successor인 경우입니다.

```
    node                    next_node
    /  \                     /   \
   A   next_node    ──►     A    next_node.right
         \
          next_node.right
```

이때는 `next_node`가 이미 `node.right` 서브트리 전체(= `next_node.right`)를 데리고 있으므로 손댈 게 없습니다. 바로 `if next_node is not node.right:` 블록을 건너뜁니다.

**(b) `next_node`가 더 깊이 있는 경우** — `node.right`의 왼쪽 스파인을 타고 내려가야 successor를 찾을 수 있는, 더 일반적인 경우입니다.

```
        node
       /    \
      A      R  (= node.right)
              \
              ...
             /
            P
           /
      next_node
           \
        next_node.right
```

```python
if next_node is not node.right:
    self._transplant(next_node, next_node.right)   # ① next_node를 원래 자리에서 뽑아낸다
    next_node.set_right(node.right)                 # ② node의 오른쪽 서브트리 전체를 next_node에 붙인다
```

- ① `_transplant(next_node, next_node.right)` — `next_node`는 정의상(successor이므로) 왼쪽 자식이 없습니다. 그래서 오른쪽 자식(`next_node.right`, 있을 수도 없을 수도)만 신경 쓰면 됩니다. `next_node`의 부모가 이제 `next_node.right`를 대신 가리키게 되면서, `next_node`는 트리에서 완전히 분리됩니다.
- ② 트리에서 빠져나온 `next_node`의 오른쪽 자리에, `node`의 원래 오른쪽 서브트리(`R`) 전체를 붙입니다. (`node.right`는 아직 옛 값을 가리키고 있으므로 유효한 참조입니다.)

**두 경우 공통으로 이어지는 마무리:**

```python
self._transplant(node, next_node)   # node의 자리를 next_node로 갈아 끼운다
next_node.set_left(node.left)       # node의 왼쪽 서브트리를 next_node에 붙인다
```

`node`가 있던 자리를 `next_node`로 교체하고, `node`의 왼쪽 서브트리를 `next_node`의 왼쪽에 붙이면 완성입니다. (오른쪽은 이미 (a)/(b)에서 처리됐습니다.)

#### 왜 (a)/(b)를 나눠야 하는가?

(b)의 두 줄을 (a)에서도 그대로 실행하면 무슨 일이 벌어질까요? `next_node`가 `node.right` 자신이라면, `_transplant(next_node, next_node.right)`가 `node.right` 쪽 링크(=`next_node`의 부모, 즉 `node`)를 `next_node.right`로 바꿔버립니다. 그 직후 `next_node.set_right(node.right)`를 하면, 이때의 `node.right`는 이미 위에서 망가진 값을 가리키고 있어서 **자기 자신을 참조하는 순환 포인터**가 생겨버립니다. 그래서 `next_node is not node.right`로 이 특수 케이스를 반드시 걸러내야 합니다.

### 5-3. 삭제 예시 (케이스 3, (b))

```
5, 3, 8, 6, 7, 9 삽입 후 5 삭제:

        5                          6
       / \                        / \
      3   8      -- 삭제(5) -->  3   8
         / \                        / \
        6   9                      7   9
         \
          7
```

- `next_node = successor(5) = 6` (`5.right = 8`의 최솟값), `6 != 8` → (b) 케이스
- ① `_transplant(6, 7)`: `8.left = 7`
- ② `6.set_right(8)`: `6.right = 8`, `8.parent = 6`
- `_transplant(5, 6)`: `root = 6`
- `6.set_left(3)`: `6.left = 3`, `3.parent = 6`

결과: `root=6, 6.left=3, 6.right=8, 8.left=7, 8.right=9` — 올바른 BST.

### 5-4. Successor / Predecessor

`_delete_node`의 케이스 3에서 쓰는 `successor(node)`는 "이 노드보다 딱 한 단계 큰 값의 노드"를 찾습니다.

```python
@classmethod
def successor(cls, node: BSTNode[T]) -> BSTNode[T] | None:
    if node.right is not None:
        return cls.find_min_node(node.right)

    # 오른쪽 자식이 없으면, 조상 중 하나가 successor다.
    current, parent = node, node.parent
    while parent is not None and current is parent.right:
        current, parent = parent, parent.parent

    return parent
```

- 오른쪽 자식이 있으면 → 그 서브트리에서 가장 작은 값(`find_min_node`)이 successor.
- 오른쪽 자식이 없으면 → "내가 부모의 오른쪽 자식인 동안" 계속 위로 올라간다. 루프가 멈췄을 때, 남아있는 `parent`가 있다면 그건 내가 **왼쪽 자식**이었기 때문에 멈춘 것이고, 그 조상이 바로 successor다.

`predecessor`는 좌우를 뒤집은 완전한 대칭입니다.

## 6. 시간복잡도

| 연산 | 일반 BST (평균) | 일반 BST (최악, 편향 트리) |
|---|---|---|
| 탐색 (find) | `O(log n)` | `O(n)` |
| 삽입 (insert) | `O(log n)` | `O(n)` |
| 삭제 (delete) | `O(log n)` | `O(n)` |

`_transplant`, `set_left`/`set_right` 자체는 포인터 몇 개만 바꾸는 `O(1)` 연산입니다. 이 문서의 BST는 스스로 균형을 맞추지 않으므로, 삽입 순서가 나쁘면(예: 정렬된 배열을 그대로 삽입) 최악의 경우로 치우칠 수 있습니다 — 이 문제를 해결하는 것이 [`AVL_TREE.md`](./AVL_TREE.md), [`RED_BLACK_TREE.md`](./RED_BLACK_TREE.md)의 주제입니다.

## 7. 개념 ↔ 코드 대응표

| 개념 | 코드 위치 |
|---|---|
| 노드, 부모 포인터 | `BSTNode` (`binary_search_tree.py:11`) |
| 자식 연결 + parent 동기화 | `BSTNode.set_left` / `set_right` (`binary_search_tree.py:39`, `44`) |
| 재귀/루프 경로 분기 기준 | `_insert`, `_delete`, `_find` (`binary_search_tree.py:142`, `197`, `110`) |
| 삽입 (재귀) | `_insert_by_recursive` (`binary_search_tree.py:148`) |
| 삽입 위치 탐색 (루프) | `find_leaf_node_having_value` (`binary_search_tree.py:83`) |
| 삽입 (루프, 실제 연결) | `_insert_node_into_parent_node` (`binary_search_tree.py:182`) |
| 자리 교체의 핵심 연산 | `_transplant` (`binary_search_tree.py:261`) |
| 삭제의 3가지 케이스 | `_delete_node` (`binary_search_tree.py:232`) |
| successor / predecessor | `successor`, `predecessor` (`binary_search_tree.py:299`, `319`) |

## 8. 직접 실행해보기

```bash
python3 -m algorithm.binarysearch.binary_search_tree
```

`__main__` 데모에서 정렬된 배열을 그대로 삽입했을 때 트리 높이가 `n`까지 치솟는 것(사실상 연결 리스트)을 확인할 수 있습니다. 같은 값을 `AVLTree`/`RedBlackTree`에 넣었을 때와 비교해보면 균형 유지의 효과가 뚜렷하게 보입니다.

---

[◀ 이전: 이진 트리](./BINARY_TREE.md) | [다음: AVL 트리 ▶](./AVL_TREE.md)
