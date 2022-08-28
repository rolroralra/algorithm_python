from sys import stdin
new_input = stdin.readline

if __name__ == '__main__':

    is_prime = [True] * 10_001

    is_prime[0] = False
    is_prime[1] = False
    for i in range(2, len(is_prime)):
        if not is_prime[i]:
            continue

        for j in range(i * i, len(is_prime), i):
            is_prime[j] = False

    t = int(new_input())
    for test_case in range(t):
        n = int(new_input())
        for a in range(n // 2, 1, -1):
            b = n - a
            if is_prime[a] and is_prime[b]:
                print(f'{a} {b}')
                break

