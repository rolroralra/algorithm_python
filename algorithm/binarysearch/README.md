# algorithm/binarysearch — 인덱스

이 디렉토리는 "정렬/탐색 범위를 절반씩 줄여나간다"는 이진 탐색의 아이디어를, 배열 위에서(이진 탐색)부터 자가 균형 트리(AVL, Red-Black)까지 단계적으로 확장해가며 구현합니다.

## 문서 목록

| 순서 | 문서 | 다루는 구현 | 핵심 내용 |
|---|---|---|---|
| 1 | [`BINARY_SEARCH.md`](./BINARY_SEARCH.md) | `binarysearch.py`, `lower_bound.py`, `upper_bound.py` | 배열에서의 이진 탐색, `lower_bound`/`upper_bound`로 중복 구간의 경계 찾기 |
| 2 | [`BINARY_TREE.md`](./BINARY_TREE.md) | `binary_tree.py` | 이진 트리의 기본기: 노드 구조, 전위/중위/후위 순회, 높이. BST/AVL/RBT가 공통 상속하는 베이스 클래스 |
| 3 | [`BINARY_SEARCH_TREE.md`](./BINARY_SEARCH_TREE.md) | `binary_search_tree.py` | "왼쪽은 작게, 오른쪽은 크게" 규칙의 이진 탐색 트리(BST). 삽입/삭제/successor. 균형이 깨질 수 있다는 한계 |
| 4 | [`AVL_TREE.md`](./AVL_TREE.md) | `avl_tree.py` | balance factor와 회전(rotation)으로 매번 균형을 엄격하게 맞추는 자가 균형 BST |
| 5 | [`RED_BLACK_TREE.md`](./RED_BLACK_TREE.md) | `red_black_tree.py` | 색(RED/BLACK) 규칙으로 균형을 느슨하게 유지하는 자가 균형 BST. AVL과의 트레이드오프 비교 |

## 권장 읽기 순서

```
BINARY_SEARCH.md  →  BINARY_TREE.md  →  BINARY_SEARCH_TREE.md  →  AVL_TREE.md  →  RED_BLACK_TREE.md
 (배열 이진 탐색)      (트리 기초)          (BST)                   (균형 트리 1)      (균형 트리 2)
```

- **이진 탐색 개념**을 배열 위에서 먼저 익히고,
- 그 개념을 **트리라는 자료구조**(순회, 높이) 위로 옮긴 뒤,
- "왼쪽은 작게, 오른쪽은 크게"라는 규칙을 더해 **BST**를 만들고,
- BST가 삽입 순서에 따라 한쪽으로 치우칠 수 있다는 한계를 확인한 뒤,
- 이를 해결하는 두 가지 **자가 균형 트리**(AVL → Red-Black 순, 엄격한 균형에서 느슨한 균형으로)를 비교하며 봅니다.

각 문서 하단에는 이 순서를 따르는 "이전 문서 | 다음 문서" 네비게이션 링크가 있습니다.

## 관련 테스트

```bash
pytest tests/binarysearch/ -v
```
