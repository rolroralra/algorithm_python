import pytest

from algorithm.euclidean.euler_phi import EulerPhi


@pytest.mark.unit
class TestEulerPhiSieve:
    def test_known_value(self):
        phi = EulerPhi()
        assert phi(45) == 24

    def test_phi_of_one_is_one(self):
        assert EulerPhi()(1) == 1

    def test_phi_of_prime_is_prime_minus_one(self):
        assert EulerPhi()(17) == 16

    def test_phi_of_two(self):
        assert EulerPhi()(2) == 1

    def test_reinitializes_when_queried_beyond_current_range(self):
        phi = EulerPhi()
        phi(6)

        assert phi(45) == 24


@pytest.mark.unit
class TestEulerPhiByFactorization:
    def test_known_value(self):
        assert EulerPhi().phi_by_factorization(45) == 24

    def test_phi_of_one_is_one(self):
        assert EulerPhi().phi_by_factorization(1) == 1

    def test_phi_of_prime_is_prime_minus_one(self):
        assert EulerPhi().phi_by_factorization(17) == 16

    @pytest.mark.parametrize("n", range(2, 100))
    def test_matches_sieve_based_computation(self, n):
        assert EulerPhi().phi_by_factorization(n) == EulerPhi()(n)
