from find_sum import BST, build_bst, find_sum


def run_tests() -> None:
    empty = BST()
    assert find_sum(empty) == 0

    single = build_bst([42])
    assert find_sum(single) == 42

    assert find_sum(build_bst([50, 30, 70, 20, 40, 60, 80, 10])) == 360
    assert find_sum(build_bst([1, 2, 3, 4, 5])) == 15
    assert find_sum(build_bst([5, 4, 3, 2, 1])) == 15

    assert find_sum(build_bst([-1, -2, -3])) == -6
    assert find_sum(build_bst([0, -5, 5])) == 0
    assert find_sum(build_bst([10, -10])) == 0

    # duplicates ignored on insert — sum reflects unique values
    assert find_sum(build_bst([5, 5, 5])) == 5
    assert find_sum(build_bst([1, 2, 1, 3, 2])) == 6

    print("All tests passed!")


if __name__ == "__main__":
    run_tests()
