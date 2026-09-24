# 이진 트리 (Binary Tree)

> 구현: [`binary_tree.py`](./binary_tree.py) — `BinaryTreeNode`, `BinaryTree` 클래스
> 이 문서에서 다루는 `BinaryTreeNode`/`BinaryTree`는 [`BINARY_SEARCH_TREE.md`](./BINARY_SEARCH_TREE.md), [`AVL_TREE.md`](./AVL_TREE.md), [`RED_BLACK_TREE.md`](./RED_BLACK_TREE.md)가 **공통으로 상속하는 가장 밑바탕 클래스**입니다. 이 문서를 먼저 읽어두면 세 문서에서 "traversal", "height" 같은 용어가 나올 때 바로 이해할 수 있습니다.

## 1. 왜 이진 트리가 필요한가?

배열이나 연결 리스트는 원소들이 일렬로 늘어서 있습니다. 그런데 데이터에 "부모-자식" 같은 계층 구조가 있거나, 탐색할 때마다 절반씩 후보를 줄여나가고 싶다면 일렬 구조로는 표현하기 불편합니다.

**이진 트리(binary tree)** 는 각 노드가 최대 2개의 자식(왼쪽/오른쪽)만 갖는 트리 구조입니다. 이 단순한 규칙 하나로:

- 계층적 데이터(조직도, 파일 시스템, 수식 트리 등)를 자연스럽게 표현할 수 있고
- (자식이 2개뿐이므로) 각 노드를 방문하는 순서를 몇 가지 정해진 패턴으로 체계화할 수 있으며
- 값의 크기 순서라는 규칙을 추가하면 [이진 탐색 트리(BST)](./BINARY_SEARCH_TREE.md)가 되어, 배열의 이진 탐색과 같은 `O(log n)` 탐색을 "삽입/삭제가 가능한 자료구조" 위에서 할 수 있게 됩니다.

`binary_tree.py`는 이런 응용들이 공통으로 필요로 하는 최소한의 기능 — **노드 구조, 순회(traversal), 높이(height), 출력** — 만 담은 "기초 공사"에 해당합니다.

## 2. 노드 구조: `BinaryTreeNode`

```python
# binary_tree.py:6-15
class BinaryTreeNode(Generic[T]):
    def __init__(self, value: T):
        self.value = value
        self.left: 'BinaryTreeNode[T] | None' = None
        self.right: 'BinaryTreeNode[T] | None' = None
```

`value`, `left`, `right` 세 필드만 가진 아주 얕은(shallow) 노드입니다. 일부러 최소한으로 설계되어 있습니다 — 파일 상단 주석(`binary_tree.py:7-9`)에 적혀 있듯, `parent` 포인터([`BSTNode`](./BINARY_SEARCH_TREE.md)), `height`([`AVLNode`](./AVL_TREE.md)), `color`([`RBNode`](./RED_BLACK_TREE.md)) 같은 트리별 확장 필드는 여기 두지 않고, 각 서브클래스가 `BinaryTreeNode`를 상속해서 필요한 만큼만 덧붙입니다.

```
BinaryTreeNode  (value, left, right)
     ▲  ▲  ▲
     │  │  └── RBNode        (+ color)              → RED_BLACK_TREE.md
     │  └───── AVLNode       (+ height)              → AVL_TREE.md
     └──────── BSTNode       (+ parent, 질의 메서드)  → BINARY_SEARCH_TREE.md
```

즉 `binary_tree.py`가 정의하는 `inorder()`/`preorder()`/`postorder()`/`height()`/`print_tree()`는 이 네 트리 클래스 모두에서 **그대로 상속되어 재사용**됩니다.

## 3. 트리 순회 (Traversal)

노드를 방문하는 순서에 따라 세 가지 기본 순회가 있습니다. 예시로 다음 트리를 사용합니다 (`binary_tree.py:89-93`의 `__main__` 데모와 동일):

```
        1
       / \
      2   3
     / \
    4   5
```

| 순회 | 방문 순서 | 결과 | 규칙 |
|---|---|---|---|
| 전위 (preorder) | 나 → 왼쪽 → 오른쪽 | `1, 2, 4, 5, 3` | 노드를 먼저 처리하고 자식으로 내려감 |
| 중위 (inorder) | 왼쪽 → 나 → 오른쪽 | `4, 2, 5, 1, 3` | 왼쪽을 다 처리한 뒤 나, 그다음 오른쪽 |
| 후위 (postorder) | 왼쪽 → 오른쪽 → 나 | `4, 5, 2, 3, 1` | 자식을 모두 처리한 뒤 마지막에 나 |

세 순회 모두 구조가 완전히 동일한 재귀 함수이고, **`action(node)`를 호출하는 위치만 다릅니다**:

```python
# binary_tree.py:43-50 (inorder)
def _inorder(self, node, action=...):
    if node is None:
        return
    self._inorder(node.left, action)
    action(node)                        # ← 가운데
    self._inorder(node.right, action)

# binary_tree.py:52-59 (preorder) — action이 맨 앞
# binary_tree.py:61-68 (postorder) — action이 맨 뒤
```

`action`은 기본값으로 `print(x, end=' ')`가 들어가 있지만(`binary_tree.py:44`), `inorder()`/`preorder()`/`postorder()`(`binary_tree.py:22-35`)는 콜백으로 리스트에 값을 append하는 람다를 넘겨서 **결과를 리스트로 모아 반환**합니다. 이렇게 "방문했을 때 무엇을 할지"를 분리해두면, 나중에 [`BINARY_SEARCH_TREE.md`](./BINARY_SEARCH_TREE.md)에서 보듯 inorder 순회가 "정렬된 순서로 값 나열하기"에도 그대로 재사용됩니다 — BST에서는 inorder 순회 결과가 항상 오름차순 정렬이기 때문입니다.

> 참고: 레벨 순서(BFS) 순회는 `binary_tree.py`에는 구현되어 있지 않습니다. 현재는 전위/중위/후위 세 가지 DFS 기반 순회만 제공합니다.

## 4. 높이 (Height)

```python
# binary_tree.py:70-74
def _height(self, node):
    if node is None:
        return 0
    return 1 + max(self._height(node.left), self._height(node.right))
```

빈 트리(`None`)의 높이는 `0`, 리프 노드 하나만 있어도 높이는 `1`입니다. 이 트리 전체를 순회해야 하므로 `height()`는 `O(n)`이 걸립니다 (`n`은 노드 개수).

```
        1              height(1) = 1 + max(height(2), height(3))
       / \                        = 1 + max(2, 1) = 3
      2   3            height(2) = 1 + max(height(4), height(5)) = 1 + max(1,1) = 2
     / \                height(3) = 1
    4   5                height(4) = height(5) = 1 (리프)
```

이 `O(n)` 높이 계산은 나중에 [`AVL_TREE.md`](./AVL_TREE.md)에서 중요한 비교 대상이 됩니다 — AVL 트리는 매 삽입/삭제마다 균형을 확인해야 하는데, 그때마다 `height()`를 `O(n)`으로 다시 계산하면 전체가 `O(n log n)`으로 느려지므로, `AVLNode`는 높이를 필드에 캐싱해서 `O(1)`에 읽습니다. 즉 이 `_height()`는 "가장 단순하지만 느린" 기준선입니다.

## 5. 트리 출력: `print_tree()`

`_print_tree()`(`binary_tree.py:76-86`)는 오른쪽 서브트리를 먼저(위쪽에), 왼쪽 서브트리를 나중에(아래쪽에) 재귀적으로 출력해서, 터미널에서도 트리 모양이 눈에 보이도록 `└──`/`┌──` 문자로 그려줍니다. 이 메서드 역시 BST/AVL/RBT가 그대로 상속해서 사용합니다 — `AVL_TREE.md`, `RED_BLACK_TREE.md`의 데모에서 출력되는 트리 그림이 바로 이 함수의 결과물입니다.

## 6. 시간/공간복잡도

| 연산 | 시간복잡도 | 비고 |
|---|---|---|
| `inorder()` / `preorder()` / `postorder()` | `O(n)` | 모든 노드를 한 번씩 방문 |
| `height()` | `O(n)` | 매번 서브트리를 새로 순회 (캐싱 없음) |
| `print_tree()` | `O(n)` | 순회 기반 |
| 공간 (재귀 호출 스택) | `O(h)` | `h`는 트리 높이. 균형 트리면 `O(log n)`, 한쪽으로 치우치면 `O(n)` |

## 7. 개념 ↔ 코드 대응표

| 개념 | 코드 위치 |
|---|---|
| 최소 공통 노드 (value/left/right) | `BinaryTreeNode` (`binary_tree.py:6`) |
| 트리 컨테이너 (root 보관) | `BinaryTree` (`binary_tree.py:18`) |
| 전위 순회 | `preorder()` → `_preorder()` (`binary_tree.py:27`, `52`) |
| 중위 순회 | `inorder()` → `_inorder()` (`binary_tree.py:22`, `43`) |
| 후위 순회 | `postorder()` → `_postorder()` (`binary_tree.py:32`, `61`) |
| 트리 높이 (O(n)) | `height()` → `_height()` (`binary_tree.py:37`, `70`) |
| ASCII 트리 출력 | `print_tree()` → `_print_tree()` (`binary_tree.py:40`, `76`) |

## 8. 직접 실행해보기

```bash
python3 -m algorithm.binarysearch.binary_tree
```

`__main__` 데모(`binary_tree.py:88-101`)에서 위 예시와 동일한 트리를 만들어 세 가지 순회 결과와 높이, ASCII 트리 출력을 한 번에 확인할 수 있습니다.

---

[◀ 이전: 이진 탐색](./BINARY_SEARCH.md) | [다음: 이진 탐색 트리 ▶](./BINARY_SEARCH_TREE.md)
