from coins import COINS, find_coins_greedy, find_min_coins


def total_coins(d: dict[int, int]) -> int:
    return sum(d.values())


def total_value(d: dict[int, int]) -> int:
    return sum(coin * count for coin, count in d.items())


def run_tests() -> None:
    # zero amount — empty result
    assert find_coins_greedy(0) == {}
    assert find_min_coins(0) == {}

    # canonical example from the task
    assert find_coins_greedy(113) == {50: 2, 10: 1, 2: 1, 1: 1}
    assert find_min_coins(113) == {50: 2, 10: 1, 2: 1, 1: 1}

    # single coin denominations
    assert find_coins_greedy(50) == {50: 1}
    assert find_coins_greedy(1) == {1: 1}
    assert find_min_coins(50) == {50: 1}

    # both algorithms must always sum back to the amount
    for amount in [1, 2, 3, 7, 49, 50, 51, 99, 100, 113, 999, 1234, 9999]:
        g = find_coins_greedy(amount)
        d = find_min_coins(amount)
        assert total_value(g) == amount, (amount, g)
        assert total_value(d) == amount, (amount, d)

        # for the canonical Ukrainian/Euro-like system, greedy is optimal:
        # DP must give exactly the same number of coins
        assert total_coins(d) == total_coins(g), (
            f"on canonical coin set greedy should match DP: "
            f"amount={amount}, greedy={total_coins(g)}, dp={total_coins(d)}"
        )

    # non-canonical coin set where greedy is suboptimal
    weird = [1, 3, 4]
    # amount 6: greedy = 4+1+1 (3 coins), DP = 3+3 (2 coins)
    g = find_coins_greedy(6, weird)
    d = find_min_coins(6, weird)
    assert total_value(g) == 6 and total_value(d) == 6
    assert total_coins(g) == 3
    assert total_coins(d) == 2
    assert d == {3: 2}

    # negative amount — raises
    try:
        find_coins_greedy(-1)
        assert False, "expected ValueError"
    except ValueError:
        pass
    try:
        find_min_coins(-1)
        assert False, "expected ValueError"
    except ValueError:
        pass

    # unreachable amount with limited coin set
    try:
        find_min_coins(3, [2, 4])
        assert False, "expected ValueError for unreachable amount"
    except ValueError:
        pass

    print("All tests passed!")


if __name__ == "__main__":
    run_tests()
