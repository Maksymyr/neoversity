import random

from sort_benchmark import (
    insertion_sort,
    merge_sort,
    timsort,
    make_random,
    make_sorted,
    make_reversed,
    make_nearly_sorted,
)


def run_tests() -> None:
    for algorithm in (insertion_sort, merge_sort, timsort):
        assert algorithm([]) == []
        assert algorithm([1]) == [1]
        assert algorithm([3, 1, 2]) == [1, 2, 3]
        assert algorithm([5, 5, 5]) == [5, 5, 5]
        assert algorithm([2, -1, 0, 4, -3]) == [-3, -1, 0, 2, 4]

    random.seed(0)
    for _ in range(20):
        n = random.randint(0, 200)
        data = [random.randint(-100, 100) for _ in range(n)]
        before = data[:]
        expected = sorted(data)
        assert insertion_sort(data) == expected
        assert merge_sort(data) == expected
        assert timsort(data) == expected
        assert data == before, "input list must not be mutated"

    for builder, expected_len in (
        (make_random, 50),
        (make_sorted, 50),
        (make_reversed, 50),
        (make_nearly_sorted, 50),
    ):
        data = builder(expected_len)
        assert len(data) == expected_len
        assert merge_sort(data) == sorted(data)

    assert make_sorted(5) == [0, 1, 2, 3, 4]
    assert make_reversed(5) == [5, 4, 3, 2, 1]

    print("All tests passed!")


if __name__ == "__main__":
    run_tests()
