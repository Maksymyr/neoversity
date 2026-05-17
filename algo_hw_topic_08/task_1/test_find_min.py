from find_min import BST, build_bst, find_min


def run_tests() -> None:
    empty = BST()
    try:
        find_min(empty)
        assert False, "expected ValueError on empty tree"
    except ValueError:
        pass

    single = build_bst([42])
    assert find_min(single) == 42

    assert find_min(build_bst([50, 30, 70, 20, 40, 60, 80, 10])) == 10
    assert find_min(build_bst([5, 3, 8, 1, 4, 7, 9])) == 1
    assert find_min(build_bst([1, 2, 3, 4, 5])) == 1
    assert find_min(build_bst([5, 4, 3, 2, 1])) == 1

    assert find_min(build_bst([0, -10, 10, -20, -5])) == -20
    assert find_min(build_bst([-1])) == -1

    assert find_min(build_bst([7, 7, 7])) == 7
    assert find_min(build_bst([5, 3, 5, 3, 1, 1])) == 1

    print("All tests passed!")


if __name__ == "__main__":
    run_tests()
