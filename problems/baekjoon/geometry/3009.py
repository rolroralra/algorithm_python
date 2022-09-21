from sys import stdin

readline = stdin.readline

if __name__ == '__main__':
    input_set = set([tuple(map(int, readline().split(" "))) for i in range(3)])

    x_list = list(map(lambda p: p[0], input_set))
    y_list = list(map(lambda p: p[1], input_set))

    x_max = max(x_list)
    x_min = min(x_list)
    y_max = max(y_list)
    y_min = min(y_list)

    total_set = {(x_max, y_max), (x_max, y_min), (x_min, y_max), (x_min, y_min)}

    for p in total_set - input_set:
        print(f"{p[0]} {p[1]}")
        break
