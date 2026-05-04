import random
import timeit
from typing import Callable

from colorama import Fore, init

init(autoreset=True)


def insertion_sort(arr: list[int]) -> list[int]:
    a = arr[:]
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


def merge_sort(arr: list[int]) -> list[int]:
    if len(arr) <= 1:
        return arr[:]
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)


def _merge(left: list[int], right: list[int]) -> list[int]:
    result: list[int] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def timsort(arr: list[int]) -> list[int]:
    return sorted(arr)


def make_random(n: int) -> list[int]:
    return [random.randint(0, 1_000_000) for _ in range(n)]


def make_sorted(n: int) -> list[int]:
    return list(range(n))


def make_reversed(n: int) -> list[int]:
    return list(range(n, 0, -1))


def make_nearly_sorted(n: int) -> list[int]:
    data = list(range(n))
    swaps = max(1, n // 100)
    for _ in range(swaps):
        i, j = random.randrange(n), random.randrange(n)
        data[i], data[j] = data[j], data[i]
    return data


DATASETS: dict[str, Callable[[int], list[int]]] = {
    "random": make_random,
    "sorted": make_sorted,
    "reversed": make_reversed,
    "nearly_sorted": make_nearly_sorted,
}

ALGORITHMS: dict[str, Callable[[list[int]], list[int]]] = {
    "insertion": insertion_sort,
    "merge":     merge_sort,
    "timsort":   timsort,
}

SIZES = (100, 1_000, 10_000, 100_000, 1_000_000)
INSERTION_LIMIT = 10_000
REPEATS = 3


def measure(algorithm: Callable[[list[int]], list[int]], data: list[int]) -> float:
    timer = timeit.Timer(lambda: algorithm(data))
    times = timer.repeat(repeat=REPEATS, number=1)
    return min(times)


def format_seconds(seconds: float) -> str:
    if seconds < 1e-3:
        return f"{seconds * 1e6:>9.2f} µs"
    if seconds < 1.0:
        return f"{seconds * 1e3:>9.2f} ms"
    return f"{seconds:>9.4f}  s"


def run_benchmark() -> None:
    random.seed(42)
    print(f"{Fore.MAGENTA}Sorting benchmark — best of {REPEATS} runs\n")

    for dataset_name, builder in DATASETS.items():
        print(f"{Fore.CYAN}=== dataset: {dataset_name} ===")
        header = f"{'size':>8} | " + " | ".join(f"{name:>13}" for name in ALGORITHMS)
        print(header)
        print("-" * len(header))

        for size in SIZES:
            data = builder(size)
            row = [f"{size:>8}"]
            for algo_name, algo in ALGORITHMS.items():
                if algo_name == "insertion" and size > INSERTION_LIMIT:
                    row.append(f"{'skipped':>13}")
                    continue
                elapsed = measure(algo, data)
                row.append(f"{format_seconds(elapsed):>13}")
            print(" | ".join(row))
        print()


if __name__ == "__main__":
    run_benchmark()
