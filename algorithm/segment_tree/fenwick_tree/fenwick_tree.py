class FenwickTree:
    BASE_INDEX = 1

    def __init__(self, size):
        assert size > 0

        self.size = size + 1
        self.tree = [0] * (size + 1)

    def query(self, start_index: int, end_index: int):
        return self.__query(end_index) - self.__query(start_index - 1)


    def __query(self, index: int):
        result = 0
        while index > 0:
            result += self.tree[index]

            index -= (index & -index)

        return result


    def update(self, index: int, diff: int):
        while index < self.size:
            self.tree[index] += diff
            index += (index & -index)
