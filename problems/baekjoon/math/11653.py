import math
from sys import stdin

new_input = stdin.readline

if __name__ == '__main__':
    n = int(new_input())

    is_prime = [True] * (n + 1)

    is_prime[0] = False
    is_prime[1] = False

    prime_list = []

    for i in range(2, int(math.sqrt(len(is_prime)) + 1)):
        if not is_prime[i]:
            continue

        prime_list.append(i)

        for j in range(i * i, len(is_prime), i):
            is_prime[j] = False

    for i in range(int(math.sqrt(len(is_prime))) + 1, len(is_prime)):
        if is_prime[i]:
            prime_list.append(i)

    for prime in prime_list:
        if n == 1:
            break

        while n % prime == 0:
            print(prime)
            n //= prime

