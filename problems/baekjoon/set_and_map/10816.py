from sys import stdin

new_input = stdin.readline

if __name__ == '__main__':
    n = int(new_input())
    card_count_dict = dict()

    for card in list(map(int, new_input().split(" "))):
        card_count_dict[card] = card_count_dict.get(card, 0) + 1

    m = int(new_input())

    print(" ".join([str(card_count_dict.get(input_card, 0)) for input_card in list(map(int, new_input().split(" ")))]))
