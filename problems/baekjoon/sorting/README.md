# Sorting Algorithm
- [Selection Sort](#selection-sort)
- [Insertion Sort](#insertion-sort)
- [Bubble Sort](#bubble-sort)
- [Quick Sort](#quick-sort)
- [Merge Sort](#merge-sort)
- [Heap Sort](#heap-sort)

## Reference
- [https://www.toptal.com/developers/sorting-algorithms](https://www.toptal.com/developers/sorting-algorithms)
- [https://namu.wiki/w/%EC%A0%95%EB%A0%AC%20%EC%95%8C%EA%B3%A0%EB%A6%AC%EC%A6%98](https://namu.wiki/w/%EC%A0%95%EB%A0%AC%20%EC%95%8C%EA%B3%A0%EB%A6%AC%EC%A6%98)

## Time & Space Complexity
| Algorithm      | Average Time             | Best Time                | Wort Time                | Stability | Additional Memory Storage |
|----------------|--------------------------|--------------------------|--------------------------|-----------|---------------------------|
| Selection Sort | O(N\<sup\>2\</sup\>)     | O(N\<sup\>2\</sup\>)     | O(N\<sup\>2\</sup\>)     | X         | X                         |
| Insertion Sort | O(N\<sup\>2\</sup\>)     | O(N)                     | O(N\<sup\>2\</sup\>)     | O         | X                         |
| Bublle Sort    | O(N\<sup\>2\</sup\>)     | O(N)                     | O(N\<sup\>2\</sup\>)     | O         | X                         |
| Quick Sort     | O(Nlog\<sub\>2\</sub\>N) | O(Nlog\<sub\>2\</sub\>N) | O(N\<sup\>2\</sup\>)     | X         | X                         |
| Merge Sort     | O(Nlog\<sub\>2\</sub\>N) | O(Nlog\<sub\>2\</sub\>N) | O(Nlog\<sub\>2\</sub\>N) | O         | O                         |
| Heap Sort      | O(Nlog\<sub\>2\</sub\>N) | O(Nlog\<sub\>2\</sub\>N) | O(Nlog\<sub\>2\</sub\>N) | X         | X                         |
| Radix Sort     | O(dN)                    | O(dN)                    | O(dN)                    | O         | O                         |
| Shell Sort     | O(N\<sup\>1.5\</sup\>)   | O(N)                     | O(N\<sup\>2\</sup\>)     | X         | X                         |
---
## Selection Sort
- 
```python
def selection_sort(arr, left, right, comp):
    for i in range(left, right):
        min_index = i
        min_value = arr[i]
        for j in range(i + 1, right + 1):
            if comp(min_value, arr[j]) > 0:
                min_index = j
                min_value = arr[j]

        if i != min_index:
            arr[i], arr[min_index] = arr[min_index], arr[i]
```

## Insertion Sort
```python
def insertion_sort(arr, left, right, comp):
    for i in range(left + 1, right + 1):
        for j in range(i, left, -1):
            if comp(arr[j - 1], arr[j]) <= 0:
                break

            arr[j - 1], arr[j] = arr[j], arr[j - 1]
```

## Bubble Sort
```python
def bubble_sort(arr, left, right, comp):
    for i in range(right - left):
        is_swapped = False
        for j in range(left, right - i):
            if comp(arr[j], arr[j + 1]) > 0:
                is_swapped = True
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

        if not is_swapped:
            break
```

## Quick Sort
```python
def quick_sort(arr, left, right, comp):
    if left >= right:
        return

    pivot = left
    index = left
    for i in range(left + 1, right + 1):
        if comp(arr[pivot], arr[i]) > 0:
            index += 1
            if i != index:
                arr[index], arr[i] = arr[i], arr[index]

    arr[pivot], arr[index] = arr[index], arr[pivot]

    quick_sort(arr, left, index - 1, comp)
    quick_sort(arr, index + 1, right, comp)
```

## Merge Sort
```python
def merge_sort(arr, left, right, comp):
    if left >= right:
        return

    mid = (left + right) // 2
    merge_sort(arr, left, mid, comp)
    merge_sort(arr, mid + 1, right, comp)
    merge(arr, left, mid, right, comp)


def merge(arr, left, mid, right, comp):
    left_index = left
    right_index = mid + 1

    tmp = [0] * (right - left + 1)
    tmp_index = 0

    while left_index <= mid and right_index <= right:
        if comp(arr[left_index], arr[right_index]) <= 0:
            tmp[tmp_index] = arr[left_index]
            left_index += 1
        else:
            tmp[tmp_index] = arr[right_index]
            right_index += 1

        tmp_index += 1

    while left_index <= mid:
        tmp[tmp_index] = arr[left_index]
        left_index += 1
        tmp_index += 1

    while right_index <= right:
        tmp[tmp_index] = arr[right_index]
        right_index += 1
        tmp_index += 1

    for i in range(right - left + 1):
        arr[left + i] = tmp[i]
```

## Heap Sort
```python
import heapq

def heap_sort(arr, left, right, comp):
    tmp = []
    heapq.heapify(tmp)
    for v in arr:
        heapq.heappush(tmp, v)

    for i in range(left, right + 1):
        arr[i] = heapq.heappop(tmp)

    if comp(0, 1) > 0:
        arr = arr.reverse()
```