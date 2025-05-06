import math

def eratosthenes_sieve(max_number=100):
    is_prime = [True] * (max_number + 1)

    is_prime[0] = False
    is_prime[1] = False

    for i in range(2, math.isqrt(max_number) + 1):
        if not is_prime[i]:
            continue

        for j in range(i * i, max_number + 1, i):
            is_prime[j] = False

    return [number for number, is_prime in enumerate(is_prime) if is_prime]


def is_prime(number):
    return all(number % i != 0 for i in range(2, math.isqrt(number) + 1))
