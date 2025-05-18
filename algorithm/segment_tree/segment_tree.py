import operator

class SegmentTree:
    BASE_INDEX = 0

    def __init__(self, size: int, binary_operator=operator.add):
        assert size > 0

        self.size = size
        base_size = 1 << (size - 1).bit_length()
        self.base_index = base_size - 1
        self.tree_size = base_size * 2 - 1
        self.tree = [None] * self.tree_size
        self.operator = binary_operator
        self.ROOT_NODE = (self.BASE_INDEX, 0, self.size - 1)


    def update(self, target_index: int, value: int):
        self.__update_by_recursive(target_index, value, *self.ROOT_NODE)


    def __update_by_recursive(self, target_index: int, value: int, node: int, node_left_index: int, node_right_index: int):
        if node_left_index == node_right_index:
            self.tree[node] = value
            return

        left_node = node * 2 + 1
        right_node = left_node + 1
        mid_index = (node_left_index + node_right_index) // 2

        if target_index <= mid_index:
            self.__update_by_recursive(target_index, value, left_node, node_left_index, mid_index)
        else:
            self.__update_by_recursive(target_index, value, right_node, mid_index + 1, node_right_index)

        if self.tree[left_node] is not None and self.tree[right_node] is not None:
            self.tree[node] = self.operator(self.tree[left_node], self.tree[right_node])
        elif self.tree[left_node] is not None:
            self.tree[node] = self.tree[left_node]
        elif self.tree[right_node] is not None:
            self.tree[node] = self.tree[right_node]


    def query(self, start_index: int, end_index: int):
        return self.__query_by_recursive(start_index, end_index, *self.ROOT_NODE)


    def __query_by_recursive(self, start_index: int, end_index: int, node: int, node_left_index: int, node_right_index: int):
        if start_index > node_right_index or end_index < node_left_index:
            return None

        if start_index <= node_left_index and node_right_index <= end_index:
            return self.tree[node]

        left_child_node = node * 2 + 1
        right_child_node = left_child_node + 1
        mid_index = (node_left_index + node_right_index) // 2

        left_query_result = self.__query_by_recursive(start_index, end_index, left_child_node, node_left_index, mid_index)
        right_query_result = self.__query_by_recursive(start_index, end_index, right_child_node, mid_index + 1, node_right_index)

        if left_query_result is not None and right_query_result is not None:
            return self.operator(left_query_result, right_query_result)
        elif left_query_result is not None:
            return left_query_result
        elif right_query_result is not None:
            return right_query_result
        else:
            return None
