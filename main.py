if __name__ == '__main__':
    with open('sample_input.txt') as f:
        lines = [line.rstrip() for line in f]

    test_case_total_count = int(lines.pop())

    for test_case in range(test_case_total_count):
        answer = 0

        # TODO: Implementation

        print(f'#{test_case + 1} {answer}')

