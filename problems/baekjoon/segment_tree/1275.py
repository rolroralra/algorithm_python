import sys

class FenwickTree:
    BASE_INDEX = 1
    def __init__(self, size):
        self.size = size + self.BASE_INDEX
        self.tree = [0] * self.size


    def update(self, index, value):
        diff = value - self.query(index, index)

        print(f"diff={diff}")

        self.__update_by_diff(index, diff)


    def __update_by_diff(self, index, diff):
        index += self.BASE_INDEX

        while index < self.size:
            self.tree[index] += diff
            index += (index & -index)


    def query(self, start_index, end_index):
        return self.__query(end_index) - self.__query(start_index - 1)


    def __query(self, index):
        index += self.BASE_INDEX

        result = 0
        while index > 0:
            result += self.tree[index]
            index -= (index & -index)

        return result



if __name__ == '__main__':
    sys.stdin = open('sample_input.txt')
    readline = lambda: sys.stdin.readline().strip()

    N, Q = map(int, readline().split())
    arr = list(map(int, readline().split()))
    fenwick_tree = FenwickTree(N)

    for i, value in enumerate(arr):
        fenwick_tree.update(i, value)

    for _ in range(Q):
        x, y, a, b = map(int, readline().split())

        print(fenwick_tree.query(x - 1, y - 1))
        fenwick_tree.update(a - 1, b)
