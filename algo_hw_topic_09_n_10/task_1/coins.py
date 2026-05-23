import timeit

COINS = [50, 25, 10, 5, 2, 1]


def find_coins_greedy(amount: int, coins: list[int] = COINS) -> dict[int, int]:
    if amount < 0:
        raise ValueError("amount must be non-negative")
    result: dict[int, int] = {}
    for coin in sorted(coins, reverse=True):
        if amount == 0:
            break
        count, amount = divmod(amount, coin)
        if count > 0:
            result[coin] = count
    return dict(sorted(result.items()))


def find_min_coins(amount: int, coins: list[int] = COINS) -> dict[int, int]:
    if amount < 0:
        raise ValueError("amount must be non-negative")
    if amount == 0:
        return {}

    INF = amount + 1  # sentinel: "unreachable" (any real answer ≤ amount)
    dp = [INF] * (amount + 1)
    dp[0] = 0
    last_coin = [0] * (amount + 1)

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i and dp[i - coin] + 1 < dp[i]:
                dp[i] = dp[i - coin] + 1
                last_coin[i] = coin

    if dp[amount] >= INF:
        raise ValueError(f"amount {amount} cannot be formed from coins {coins}")

    result: dict[int, int] = {}
    cur = amount
    while cur > 0:
        coin = last_coin[cur]
        result[coin] = result.get(coin, 0) + 1
        cur -= coin
    return dict(sorted(result.items()))


def compare_timings(amounts: list[int], repeats: int = 3) -> None:
    print(f"\n{'amount':>10} | {'greedy (μs)':>14} | {'DP (μs)':>14} | {'DP / greedy':>12}")
    print("-" * 60)
    for amount in amounts:
        t_greedy = min(timeit.Timer(lambda a=amount: find_coins_greedy(a)).repeat(repeats, number=100)) / 100
        t_dp = min(timeit.Timer(lambda a=amount: find_min_coins(a)).repeat(repeats, number=1)) / 1
        ratio = t_dp / t_greedy
        print(f"{amount:>10} | {t_greedy * 1e6:>13.3f} | {t_dp * 1e6:>13.3f} | {ratio:>11.1f}x")


if __name__ == "__main__":
    for amount in (113, 999, 1234):
        print(f"\namount = {amount}")
        print(f"  greedy: {find_coins_greedy(amount)}")
        print(f"  DP:     {find_min_coins(amount)}")

    compare_timings([100, 1_000, 10_000, 100_000])
