from sys import stdin

new_input = stdin.readline

if __name__ == '__main__':
    n, m = map(int, new_input().split(" "))
    set_a = set([new_input().rstrip("\n") for i in range(n)])
    set_b = set([new_input().rstrip("\n") for i in range(m)])

    result_set = sorted(set_a.intersection(set_b))

    print(len(result_set))
    print("\n".join(result_set))
