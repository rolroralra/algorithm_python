def input_recursive(array, size: int, x: int, y: int):
    if size == 3:
        for i in range(x, x + 3):
            for j in range(y, y + 3):
                if i == x + 1 and j == y + 1:
                    continue

                array[i][j] = "*"
        return

    next_size = size // 3

    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1:
                continue

            next_x = x + i * next_size
            next_y = y + j * next_size
            input_recursive(array, next_size, next_x, next_y)


if __name__ == '__main__':
    n = int(input())

    array = [[" " for i in range(n)] for j in range(n)]

    input_recursive(array, n, 0, 0)

    for arr in array:
        for v in arr:
            print(v, end="")
        print()
