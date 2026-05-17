from cable_merge import min_merge_cost


def run_tests() -> None:
    assert min_merge_cost([]) == 0
    assert min_merge_cost([5]) == 0

    # two cables — single merge equals their sum
    assert min_merge_cost([3, 5]) == 8

    # classic example: [4, 3, 2, 6]
    #   merge 2+3 = 5  (total 5)
    #   merge 4+5 = 9  (total 14)
    #   merge 6+9 = 15 (total 29)
    assert min_merge_cost([4, 3, 2, 6]) == 29

    # [1..5]:
    #   1+2 = 3   (total 3)
    #   3+3 = 6   (total 9)
    #   4+5 = 9   (total 18)
    #   6+9 = 15  (total 33)
    assert min_merge_cost([1, 2, 3, 4, 5]) == 33

    # heap behavior is correct regardless of input order
    assert min_merge_cost([5, 4, 3, 2, 1]) == 33
    assert min_merge_cost([3, 1, 5, 2, 4]) == 33

    # greedy "always pick two smallest" beats other pairings on this case:
    #   wrong order (4+6 first): 4+6=10, 2+3=5, 5+10=15 → 30 - no
    #   our (2+3, then 4+5, then 6+9) → 29 - yes
    assert min_merge_cost([4, 3, 2, 6]) < 30

    # zero-length cables shouldn't break it
    # heap: [0,0,1,2] -> merge 0+0=0 (t=0) -> [0,1,2]
    #                 -> merge 0+1=1 (t=1) -> [1,2]
    #                 -> merge 1+2=3 (t=4)
    assert min_merge_cost([0, 0, 1, 2]) == 4

    # large case
    cables = [10, 5, 2, 8, 7, 3, 12, 6]
    # quick check that result is the same independent of input order
    import random
    shuffled = cables[:]
    random.seed(0)
    random.shuffle(shuffled)
    assert min_merge_cost(cables) == min_merge_cost(shuffled)

    # negative cable lengths must be rejected
    try:
        min_merge_cost([1, -1, 2])
        assert False, "expected ValueError for negative length"
    except ValueError:
        pass

    print("All tests passed!")


if __name__ == "__main__":
    run_tests()
