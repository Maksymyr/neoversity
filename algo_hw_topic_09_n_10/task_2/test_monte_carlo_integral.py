import math

import numpy as np

from monte_carlo_integral import f, monte_carlo_hit_miss, monte_carlo_mean


def run_tests() -> None:
    # exact analytical: ∫ x^2 dx from 0 to 2 = 8/3
    exact = 8 / 3

    # mean-value method converges
    for n, tolerance in [(10_000, 0.05), (100_000, 0.02), (1_000_000, 0.01)]:
        result = monte_carlo_mean(f, 0, 2, n, seed=42)
        assert abs(result - exact) < tolerance, (n, result, exact)

    # hit-or-miss method converges
    y_max = 4.0  # f(2) = 4
    for n, tolerance in [(10_000, 0.1), (100_000, 0.04), (1_000_000, 0.015)]:
        result = monte_carlo_hit_miss(f, 0, 2, y_max, n, seed=42)
        assert abs(result - exact) < tolerance, (n, result, exact)

    # both methods agree at large N
    m = monte_carlo_mean(f, 0, 2, 1_000_000, seed=0)
    hm = monte_carlo_hit_miss(f, 0, 2, y_max, 1_000_000, seed=0)
    assert abs(m - hm) < 0.02

    # different function: ∫ sin(x) dx from 0 to π = 2
    def g(x):
        return np.sin(x)

    result = monte_carlo_mean(g, 0, math.pi, 1_000_000, seed=42)
    assert abs(result - 2.0) < 0.01

    # different function: ∫ 1 dx from a to b = b - a (constant function)
    def one(x):
        return np.ones_like(x) if hasattr(x, "shape") else 1.0

    result = monte_carlo_mean(one, 3, 7, 10_000, seed=42)
    assert abs(result - 4.0) < 0.01

    # zero-width interval
    assert monte_carlo_mean(f, 1.5, 1.5, 1000, seed=42) == 0.0

    # determinism (same seed → same result)
    a = monte_carlo_mean(f, 0, 2, 10_000, seed=123)
    b = monte_carlo_mean(f, 0, 2, 10_000, seed=123)
    assert a == b

    # convergence rate: doubling N → error reduces by ~√2 on average
    # (this is a stochastic claim, so we check across several seeds)
    errors_small = []
    errors_large = []
    for seed in range(10):
        e1 = abs(monte_carlo_mean(f, 0, 2, 10_000, seed=seed) - exact)
        e2 = abs(monte_carlo_mean(f, 0, 2, 100_000, seed=seed) - exact)
        errors_small.append(e1)
        errors_large.append(e2)
    # mean error at 100k should be smaller than at 10k
    assert np.mean(errors_large) < np.mean(errors_small)

    print("All tests passed!")


if __name__ == "__main__":
    run_tests()
