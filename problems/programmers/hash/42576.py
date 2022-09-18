import collections
from sys import stdin
new_input = stdin.readline


def solution_(participant, completion):
    counter = collections.Counter(participant) - collections.Counter(completion)
    return list(counter.keys())[0]


def solution(participant, completion):
    count_dict = dict()

    for p in participant:
        count_dict[p] = count_dict.get(p, 0) + 1

    for p in completion:
        if count_dict.get(p, 0) == 0:
            continue

        count_dict[p] = count_dict[p] - 1

    for p, count in count_dict.items():
        if count > 0:
            return p


if __name__ == '__main__':
    print(solution_(["mislav", "stanko", "mislav", "ana"], ["stanko", "ana", "mislav"]))
