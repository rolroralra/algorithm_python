from sys import stdin
input = stdin.readline


def union(left: int, right: int, parent: list[int]):
    a_root = find_by_recursive(left, parent)
    b_root = find_by_recursive(right, parent)

    if a_root == b_root:
        return

    if parent[a_root] > parent[b_root]:
        a_root, b_root = b_root, a_root

    parent[a_root] += parent[b_root]
    parent[b_root] = a_root


def find_by_loop(element_index, parent):
    root = element_index
    while parent[root] >= 0:
        root = parent[root]

    index = element_index
    while index != root:
        next_index = parent[index]
        parent[index] = root
        index = next_index

    return root


def find_by_recursive(element_index, parent):
    if parent[element_index] < 0:
        return element_index

    parent[element_index] = find_by_recursive(parent[element_index], parent)
    return parent[element_index]


if __name__ == '__main__':
    n, m = map(int, input().split())

    parent_list = [-1 for i in range(n + 1)]
    for test_case in range(m):
        operation, a, b = map(int, input().split(" "))

        if operation == 0:
            union(a, b, parent_list)
        elif operation == 1:
            if a == b or find_by_recursive(a, parent_list) == find_by_recursive(b, parent_list):
                print("YES")
            else:
                print("NO")
