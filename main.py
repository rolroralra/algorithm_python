import sys

sys.stdin = open('sample_input.txt')
input = sys.stdin.readline

if __name__ == '__main__':

    test_case_total_count = int(input())

    for test_case in range(test_case_total_count):
        answer = int(input())

        # TODO: Implementation

        print(f'#{test_case + 1} {answer}')

