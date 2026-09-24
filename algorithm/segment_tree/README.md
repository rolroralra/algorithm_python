# algorithm/segment_tree — 인덱스

이 디렉토리는 "정렬된 배열의 구간(range)에 대한 쿼리(합/최솟값/최댓값 등)를 `O(log n)`에 처리하는" 자료구조 두 가지를 다룹니다 — 범용적인 **세그먼트 트리**와, 구간 합 전용으로 훨씬 가벼운 **펜윅 트리(BIT)**.

## 문서 목록

| 문서 | 다루는 구현 | 핵심 내용 |
|---|---|---|
| [`SEGMENT_TREE.md`](./SEGMENT_TREE.md) | `segment_tree.py` | 구간을 이진 트리로 감싸 `O(log n)`에 조회/갱신. 합/최솟값/최댓값 등 임의의 결합 법칙 연산 지원 |
| [`FENWICK_TREE.md`](./FENWICK_TREE.md) | `fenwick_tree/fenwick_tree.py` | `i & -i` 비트 연산만으로 구간 합을 `O(log n)`에 처리하는 경량 구조. **`binary_index_tree/binary_index_tree.py`가 실제로는 BIT가 아니라 세그먼트 트리 구현이라는 점**도 함께 정리 |

## 권장 읽기 순서

```
README.md  →  SEGMENT_TREE.md  →  FENWICK_TREE.md
(이 문서)      (범용 구간 트리)      (구간 합 전용 경량 구조 + segment_tree 대비 비교)
```

세그먼트 트리를 먼저 이해하면, 펜윅 트리가 "구간 합이라는 제약을 받아들이는 대신 얼마나 가벼워지는지"를 비교하며 읽을 수 있습니다.

## 세그먼트 트리 vs 펜윅 트리(BIT) 한눈에 비교

| 항목 | 세그먼트 트리 (`segment_tree.py`) | 펜윅 트리 (`fenwick_tree/fenwick_tree.py`) |
|---|---|---|
| 지원 연산 | 결합 법칙만 만족하면 무엇이든 (합, min, max, ...) | 역원이 있는 연산만 (합, XOR 등) — min/max 불가 |
| 조회(`query`) | `O(log n)` | `O(log n)` |
| 갱신(`update`) | `O(log n)`, **값을 대체** | `O(log n)`, **차이(diff)를 더함** |
| 인덱싱 | 0-indexed | 1-indexed |
| 공간 | `O(n)`이지만 계수가 큼 (`~4n`) | `O(n)` (`n+1`), 계수가 훨씬 작음 |
| 구현 난이도 | 재귀 + 구간 분기 로직 | 비트 연산(`i & -i`) 두 줄 |
| 이 저장소의 구현 위치 | `algorithm/segment_tree/segment_tree.py` | `algorithm/segment_tree/fenwick_tree/fenwick_tree.py` |

> ⚠️ **참고**: `algorithm/segment_tree/binary_index_tree/binary_index_tree.py`는 폴더/클래스 이름이 "이진 인덱스 트리(BIT)"를 가리키지만, 실제 구현은 비트 연산 없이 재귀로 구간을 반씩 나누는 **세그먼트 트리**입니다 (합 연산 전용으로 단순화된 버전). 자세한 비교는 [`FENWICK_TREE.md`의 7절](./FENWICK_TREE.md#7-주의-binary_index_treepy는-사실-bit가-아니다)을 참고하세요.

## 관련 테스트

```bash
pytest tests/segment_tree/ -v
```
