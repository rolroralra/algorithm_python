import sys
import collections


def check_count(request_count_map, count_map):
    return all(count_map[key] >= request_count
               for key, request_count in request_count_map.items())


if __name__ == '__main__':
    sys.stdin = open('sample_input.txt')
    readline = sys.stdin.readline

    S, P = map(int, readline().strip().split(" ", 2)[:2])

    assert S >= P

    dna_text = readline().strip()

    count_a, count_c, count_g, count_t = map(int, readline().strip().split(" ", 4)[:4])

    request_count_map = {"A": count_a, "C": count_c, "G": count_g, "T": count_t}

    count_map = collections.defaultdict(int)

    # Initialize the first window
    for c in dna_text[:P]:
        count_map[c] += 1

    # Check the first window
    result = 1 if check_count(request_count_map, count_map) else 0

    # Sliding window
    for i, curr_dna_char in enumerate(dna_text[P:]):
        prev_dna_char = dna_text[i]
        count_map[prev_dna_char] -= 1
        count_map[curr_dna_char] += 1
        result += 1 if check_count(request_count_map, count_map) else 0

    print(result)
