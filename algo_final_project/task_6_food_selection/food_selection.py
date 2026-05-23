ITEMS = {
    "pizza":     {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog":   {"cost": 30, "calories": 200},
    "pepsi":     {"cost": 10, "calories": 100},
    "cola":      {"cost": 15, "calories": 220},
    "potato":    {"cost": 25, "calories": 350},
}


def greedy_algorithm(items: dict[str, dict[str, int]], budget: int) -> dict:
    """Greedy: pick items by descending calories/cost ratio, while budget allows."""
    ranked = sorted(
        items.items(),
        key=lambda kv: kv[1]["calories"] / kv[1]["cost"],
        reverse=True,
    )
    chosen: list[str] = []
    total_cost = 0
    total_calories = 0
    for name, attrs in ranked:
        if total_cost + attrs["cost"] <= budget:
            chosen.append(name)
            total_cost += attrs["cost"]
            total_calories += attrs["calories"]
    return {"chosen": chosen, "cost": total_cost, "calories": total_calories}


def dynamic_programming(items: dict[str, dict[str, int]], budget: int) -> dict:
    """0/1 knapsack: each item is either taken or not; maximize calories under budget."""
    names = list(items.keys())
    n = len(names)

    # dp[i][b] = max calories using first i items with budget b
    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        cost = items[names[i - 1]]["cost"]
        cals = items[names[i - 1]]["calories"]
        for b in range(budget + 1):
            dp[i][b] = dp[i - 1][b]
            if cost <= b:
                take = dp[i - 1][b - cost] + cals
                if take > dp[i][b]:
                    dp[i][b] = take

    # backtrack to recover the chosen items
    chosen: list[str] = []
    b = budget
    for i in range(n, 0, -1):
        if dp[i][b] != dp[i - 1][b]:
            chosen.append(names[i - 1])
            b -= items[names[i - 1]]["cost"]
    chosen.reverse()

    total_cost = sum(items[name]["cost"] for name in chosen)
    total_calories = dp[n][budget]
    return {"chosen": chosen, "cost": total_cost, "calories": total_calories}


if __name__ == "__main__":
    for budget in (50, 75, 100, 150):
        print(f"\n=== budget = {budget} ===")
        g = greedy_algorithm(ITEMS, budget)
        d = dynamic_programming(ITEMS, budget)
        print(f"greedy:  cost={g['cost']:>3}  cal={g['calories']:>4}  items={g['chosen']}")
        print(f"DP:      cost={d['cost']:>3}  cal={d['calories']:>4}  items={d['chosen']}")
        diff = d["calories"] - g["calories"]
        if diff > 0:
            print(f"DP wins by {diff} calories ({diff / g['calories'] * 100:.1f}% better)")
        else:
            print("greedy matches DP optimum")
