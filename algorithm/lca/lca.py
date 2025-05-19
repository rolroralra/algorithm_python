class LCA:

    def __init__(self, size):
        assert size > 0
        self.size = size
        self.LOGN = (size - 1).bit_length()
        self.parent = [[-1] * (self.LOGN + 1) for _ in range(self.size)]
        self.depth = [-1] * self.size


    def build(self, adj_list: list[list[int]], root_index: int = 0):
        depth = self.depth
        parent = self.parent
        LOGN = self.LOGN
        size = self.size

        stack = []
        depth[root_index] = 0
        stack.append(root_index)
        while stack:
            curr_index= stack.pop()

            for next_index in adj_list[curr_index]:
                if depth[next_index] != -1:
                    continue

                parent[next_index][0] = curr_index
                for depth_level in range(1, LOGN + 1):
                    if parent[next_index][depth_level - 1] != -1:
                        parent[next_index][depth_level] = parent[parent[next_index][depth_level - 1]][depth_level - 1]

                depth[next_index] = depth[curr_index] + 1


    def lca(self, a, b):
        depth = self.depth
        parent = self.parent
        LOGN = self.LOGN
        size = self.size

        if depth[a] < depth[b]:
            a, b = b, a

        for depth_level in range(LOGN, -1, -1):
            if depth[a] - depth[b] >= (1 << depth_level):
                a = parent[a][depth_level]

        if a == b:
            return a

        for depth_level in range(LOGN, -1, -1):
            if parent[a][depth_level] != -1 and parent[a][depth_level] != parent[b][depth_level]:
                a = parent[a][depth_level]
                b = parent[b][depth_level]

        return parent[a][0]


    def depth(self, a):
        return self.depth[a]
