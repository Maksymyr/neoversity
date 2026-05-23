from food_selection import ITEMS, dynamic_programming, greedy_algorithm


def run_tests() -> None:
    # zero budget — nothing to take
    g = greedy_algorithm(ITEMS, 0)
    d = dynamic_programming(ITEMS, 0)
    assert g["chosen"] == [] and g["cost"] == 0 and g["calories"] == 0
    assert d["chosen"] == [] and d["cost"] == 0 and d["calories"] == 0

    # tiny budget — only pepsi (cost 10) fits among items
    g = greedy_algorithm(ITEMS, 10)
    assert g["chosen"] == ["pepsi"]
    assert g["cost"] == 10 and g["calories"] == 100
    d = dynamic_programming(ITEMS, 10)
    assert d["chosen"] == ["pepsi"]

    # budget 100 — DP must be >= greedy by definition
    for budget in (0, 5, 10, 15, 30, 50, 75, 100, 150, 200, 500):
        g = greedy_algorithm(ITEMS, budget)
        d = dynamic_programming(ITEMS, budget)
        assert d["calories"] >= g["calories"], (
            f"DP must dominate greedy at budget {budget}: "
            f"DP={d['calories']}, greedy={g['calories']}"
        )
        # cost must never exceed budget
        assert g["cost"] <= budget
        assert d["cost"] <= budget
        # cost of chosen items must sum correctly
        assert g["cost"] == sum(ITEMS[name]["cost"] for name in g["chosen"])
        assert d["cost"] == sum(ITEMS[name]["cost"] for name in d["chosen"])
        # calories of chosen must sum correctly
        assert g["calories"] == sum(ITEMS[name]["calories"] for name in g["chosen"])
        assert d["calories"] == sum(ITEMS[name]["calories"] for name in d["chosen"])

    # known answer for budget = 100
    # ratios: potato=14, cola=14.67, pepsi=10, hot-dog=6.67, hamburger=6.25, pizza=6
    # greedy picks: cola(15), potato(25)=40, then hot-dog(30)=70, then hamburger(40)=110 fail, pepsi(10)=80, pizza=130 fail
    # → greedy picks cola, potato, hot-dog, pepsi = cost 80, cal 220+350+200+100=870
    g_100 = greedy_algorithm(ITEMS, 100)
    assert g_100["cost"] == 80
    assert g_100["calories"] == 870

    # DP can do better at budget 100? Let's check: with cap 100, max calories possible
    d_100 = dynamic_programming(ITEMS, 100)
    assert d_100["calories"] >= 870

    # construction with custom items: a case where greedy is suboptimal
    # Greedy picks the high-ratio cheap item, leaving budget that doesn't fit anything good
    edge = {
        "a": {"cost": 1, "calories": 2},     # ratio 2.0 — greedy takes
        "b": {"cost": 100, "calories": 150}, # ratio 1.5
        "c": {"cost": 99, "calories": 145},  # ratio 1.464
    }
    # budget 100: greedy picks a (1, 2), then b(100) doesn't fit (1+100>100),
    # but c(99) does (1+99=100). greedy cal = 2 + 145 = 147
    # DP picks b alone (100, 150). cal = 150 — strictly better
    g_edge = greedy_algorithm(edge, 100)
    d_edge = dynamic_programming(edge, 100)
    assert g_edge["calories"] == 147
    assert d_edge["calories"] == 150
    assert d_edge["calories"] > g_edge["calories"]

    print("All tests passed!")


if __name__ == "__main__":
    run_tests()
