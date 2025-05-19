import sys
import operator

class SegmentTree:

    def __init__(self, size, binary_operator=operator.add, indentity=0):
        bit_size = (1 << (size - 1).bit_length())
        self.base_index = bit_size - 1
        self.size = 2 * bit_size - 1
        self.operator = binary_operator
        self.identity = indentity
        self.tree = [self.identity] * self.size


    def update(self, target_index, value):
        index = self.base_index + target_index
        self.tree[index] = value

        while index > 0:
            index = (index - 1) // 2
            left_index = index * 2 + 1
            right_index = left_index + 1

            self.tree[index] = self.operator(self.tree[left_index], self.tree[right_index])


    def query(self, query_start_index, query_end_index):
        left_index = self.base_index + query_start_index
        right_index = self.base_index + query_end_index

        result = self.identity
        while left_index <= right_index:
            if left_index % 2 == 0:
                result = self.operator(result, self.tree[left_index])
                left_index += 1

            if right_index % 2 == 1:
                result = self.operator(result, self.tree[right_index])
                right_index -= 1

            left_index = (left_index - 1) // 2
            right_index = (right_index - 1) // 2

        return result


MOD = 1_000_000_007

if __name__ == '__main__':
    sys.stdin = open('sample_input.txt')
    readline = lambda: sys.stdin.readline().strip()

    N, M, K = map(int, readline().split())

    tree = SegmentTree(N, lambda x, y: (x * y) % MOD, 1)

    for i in range(N):
        input_value = int(readline())
        tree.update(i, input_value)

    for _ in range(M + K):
        command, a, b = map(int, readline().split())

        if command == 1:
            tree.update(a - 1, b)
        elif command == 2:
            print(tree.query(a - 1, b - 1) % MOD)
