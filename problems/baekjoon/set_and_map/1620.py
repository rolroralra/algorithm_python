from sys import stdin
new_input = stdin.readline

if __name__ == '__main__':
    n, m = map(int, new_input().split(" "))

    monster_list = [new_input().rstrip("\n") for i in range(n)]
    monster_index_dict = {monster: i + 1 for i, monster in enumerate(monster_list)}

    input_list = [new_input().rstrip() for i in range(m)]

    for input_value in input_list:
        if input_value in monster_index_dict:
            print(monster_index_dict[input_value])
        else:
            index = int(input_value) - 1
            print(monster_list[index])
