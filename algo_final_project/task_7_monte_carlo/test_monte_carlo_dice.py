from monte_carlo_dice import THEORETICAL_PROBS, empirical_probs, simulate


def run_tests() -> None:
    # all possible sums 2..12 are represented in the theoretical table
    assert set(THEORETICAL_PROBS) == set(range(2, 13))
    # theoretical probs sum to 1
    assert abs(sum(THEORETICAL_PROBS.values()) - 1.0) < 1e-12

    # zero rolls — empty Counter
    assert simulate(0) == {}

    # deterministic with seed
    a = simulate(1000, seed=42)
    b = simulate(1000, seed=42)
    assert a == b

    # all sums are in 2..12
    counts = simulate(10_000, seed=0)
    assert all(2 <= s <= 12 for s in counts)
    assert sum(counts.values()) == 10_000

    # empirical converges to theoretical (large N)
    counts = simulate(200_000, seed=0)
    probs = empirical_probs(counts, 200_000)
    # all empirical probs sum to 1
    assert abs(sum(probs.values()) - 1.0) < 1e-12
    # each empirical prob within 1.5 percentage points of theoretical at N=200k
    # (with N=200k, std error for p=1/6 is ~0.08%, so 1.5pp is very loose — should always pass)
    for s, theo in THEORETICAL_PROBS.items():
        assert abs(probs[s] - theo) < 0.015, (s, probs[s], theo)

    # the most likely sum is 7
    assert max(THEORETICAL_PROBS, key=THEORETICAL_PROBS.get) == 7

    # distribution is symmetric around 7
    for offset in range(1, 6):
        assert THEORETICAL_PROBS[7 - offset] == THEORETICAL_PROBS[7 + offset]

    print("All tests passed!")


if __name__ == "__main__":
    run_tests()
