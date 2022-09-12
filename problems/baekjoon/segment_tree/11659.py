from sys import stdin

new_input = stdin.readline


class SegmentTree:
    def __init__(self, capacity=10):
        self.capacity = capacity

        size = 1
        while size < capacity:
            size *= 2

        size = size * 2 - 1

        self.tree = [0] * size

    def update(self, index, value):
        self.__update(index, value, 0, 0, self.capacity - 1)

    def __update(self, index, value, node, node_left_index, node_right_index):
        if index < node_left_index or node_right_index < index:
            return

        if node_left_index == node_right_index:
            self.tree[node] = value
            return

        node_mid_index = (node_left_index + node_right_index) // 2
        left_node = node * 2 + 1
        right_node = left_node + 1

        self.__update(index, value, left_node, node_left_index, node_mid_index)
        self.__update(index, value, right_node, node_mid_index + 1, node_right_index)

        self.tree[node] = self.tree[left_node] + self.tree[right_node]

    def query(self, left_index, right_index):
        return self.__query(left_index, right_index, 0, 0, self.capacity - 1)

    def __query(self, left_index, right_index, node, node_left_index, node_right_index):
        if left_index > node_right_index or right_index < node_left_index:
            return 0

        if left_index <= node_left_index and node_right_index <= right_index:
            return self.tree[node]

        node_mid_index = (node_left_index + node_right_index) // 2
        left_node = node * 2 + 1
        right_node = left_node + 1

        left_query_result = self.__query(left_index, right_index, left_node, node_left_index, node_mid_index)
        right_query_result = self.__query(left_index, right_index, right_node, node_mid_index + 1, node_right_index)

        return left_query_result + right_query_result


if __name__ == '__main__':
    n, m = map(int, new_input().split(" "))
    arr = list(map(int, new_input().rstrip("\n").split(" ")))

    segment_tree = SegmentTree(n)

    for index, value in enumerate(arr):
        segment_tree.update(index, value)

    for i in range(m):
        start, end = map(int, new_input().split(" "))
        start -= 1
        end -= 1

        if start > end:
            start, end = end, start

        print(segment_tree.query(start, end))
