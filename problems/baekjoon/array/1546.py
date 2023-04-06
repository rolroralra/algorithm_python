import sys

if __name__ == '__main__':
    getInput = sys.stdin.readline

    N = int(getInput())
    scores = list(map(int, getInput().split(" ", N)))

    result = sum(scores) * 100 / N / max(scores)

    print(f'{result:.6f}')


