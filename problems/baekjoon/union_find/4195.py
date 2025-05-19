import sys

class UnionFind:
    def __init__(self, size):
        self.parent = [-1] * size

    def union(self, a, b):
        parent = self.parent

        root_a = self.find(a)
        root_b = self.find(b)

        if root_a == root_b:
            return

        if parent[root_a] > parent[root_b]:
            root_a, root_b = root_b, root_a

        parent[root_a] += parent[root_b]
        parent[root_b] = root_a


    def find(self, a):
        parent = self.parent

        if parent[a] < 0:
            return a

        parent[a] = self.find(parent[a])
        return parent[a]


    def count(self, a):
        return self.parent[self.find(a)] * -1


if __name__ == '__main__':
    sys.stdin = open('sample_input.txt')
    readline = lambda: sys.stdin.readline().strip()

    T = int(readline())

    for t in range(T):
        F = int(readline())

        uuid = 0
        users = set()
        user_id_dict = {}

        union_find = UnionFind(2 * F)

        for _ in range(F):
            user_a, user_b = readline().split()

            if user_a not in users:
                user_id_dict[user_a] = uuid
                users.add(user_a)
                uuid += 1

            if user_b not in users:
                user_id_dict[user_b] = uuid
                users.add(user_b)
                uuid += 1

            user_a_id = user_id_dict[user_a]
            user_b_id = user_id_dict[user_b]

            union_find.union(user_a_id, user_b_id)
            print(union_find.count(user_a_id))
