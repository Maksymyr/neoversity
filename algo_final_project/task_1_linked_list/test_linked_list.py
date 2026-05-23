import random

from linked_list import LinkedList, merge_two_sorted, reverse_list, sort_list


def run_tests() -> None:
    # reverse
    assert reverse_list(LinkedList()).to_list() == []
    assert reverse_list(LinkedList.from_list([1])).to_list() == [1]
    assert reverse_list(LinkedList.from_list([1, 2])).to_list() == [2, 1]
    assert reverse_list(LinkedList.from_list([1, 2, 3, 4, 5])).to_list() == [5, 4, 3, 2, 1]
    # twice = identity
    ll = LinkedList.from_list([1, 2, 3, 4, 5])
    reverse_list(ll)
    reverse_list(ll)
    assert ll.to_list() == [1, 2, 3, 4, 5]

    # sort
    assert sort_list(LinkedList()).to_list() == []
    assert sort_list(LinkedList.from_list([1])).to_list() == [1]
    assert sort_list(LinkedList.from_list([2, 1])).to_list() == [1, 2]
    assert sort_list(LinkedList.from_list([5, 1, 4, 2, 8, 3, 7, 6])).to_list() == [1, 2, 3, 4, 5, 6, 7, 8]
    assert sort_list(LinkedList.from_list([3, 3, 1, 2, 1])).to_list() == [1, 1, 2, 3, 3]
    assert sort_list(LinkedList.from_list([-5, 0, -1, 10, -10, 3])).to_list() == [-10, -5, -1, 0, 3, 10]

    # fuzz against built-in sorted()
    random.seed(0)
    for _ in range(20):
        n = random.randint(0, 50)
        values = [random.randint(-100, 100) for _ in range(n)]
        assert sort_list(LinkedList.from_list(values)).to_list() == sorted(values)

    # merge two sorted
    assert merge_two_sorted(LinkedList(), LinkedList()).to_list() == []
    assert merge_two_sorted(LinkedList.from_list([1, 2, 3]), LinkedList()).to_list() == [1, 2, 3]
    assert merge_two_sorted(LinkedList(), LinkedList.from_list([1, 2, 3])).to_list() == [1, 2, 3]
    assert merge_two_sorted(
        LinkedList.from_list([1, 3, 5]),
        LinkedList.from_list([2, 4, 6]),
    ).to_list() == [1, 2, 3, 4, 5, 6]
    assert merge_two_sorted(
        LinkedList.from_list([1, 3, 5, 7]),
        LinkedList.from_list([2, 4, 6, 8, 10]),
    ).to_list() == [1, 2, 3, 4, 5, 6, 7, 8, 10]
    assert merge_two_sorted(
        LinkedList.from_list([1, 1, 1]),
        LinkedList.from_list([1, 1]),
    ).to_list() == [1, 1, 1, 1, 1]

    # merge fuzz
    for _ in range(20):
        a = sorted(random.randint(-50, 50) for _ in range(random.randint(0, 20)))
        b = sorted(random.randint(-50, 50) for _ in range(random.randint(0, 20)))
        assert merge_two_sorted(
            LinkedList.from_list(a),
            LinkedList.from_list(b),
        ).to_list() == sorted(a + b)

    print("All tests passed!")


if __name__ == "__main__":
    run_tests()
