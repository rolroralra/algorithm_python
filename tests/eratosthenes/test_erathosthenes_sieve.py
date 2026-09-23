import math

import pytest

from algorithm.eratosthenes.erathosthenes_sieve import eratosthenes_sieve, is_prime


def naive_primes(max_number: int) -> list[int]:
    return [n for n in range(2, max_number + 1) if all(n % i != 0 for i in range(2, math.isqrt(n) + 1))]


@pytest.mark.unit
class TestEratosthenesSieve:
    def test_no_primes_below_two(self):
        assert eratosthenes_sieve(1) == []

    def test_smallest_prime(self):
        assert eratosthenes_sieve(2) == [2]

    def test_primes_up_to_ten(self):
        assert eratosthenes_sieve(10) == [2, 3, 5, 7]

    @pytest.mark.parametrize("max_number", [30, 50, 100, 200])
    def test_matches_naive_primality_check(self, max_number):
        assert eratosthenes_sieve(max_number) == naive_primes(max_number)


@pytest.mark.unit
class TestIsPrime:
    @pytest.mark.parametrize("number", [0, 1])
    def test_numbers_below_two_are_not_prime(self, number):
        assert is_prime(number) is False

    @pytest.mark.parametrize("number", [2, 3, 5, 7, 11, 97])
    def test_known_primes(self, number):
        assert is_prime(number) is True

    @pytest.mark.parametrize("number", [4, 6, 8, 9, 15, 100])
    def test_known_composites(self, number):
        assert is_prime(number) is False

    @pytest.mark.parametrize("number", range(2, 200))
    def test_matches_sieve_for_range(self, number):
        assert is_prime(number) == (number in eratosthenes_sieve(200))
