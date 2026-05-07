import timeit
from pathlib import Path
from typing import Callable

from colorama import Fore, init

from algorithms import boyer_moore_search, kmp_search, rabin_karp_search

init(autoreset=True)


ALGORITHMS: dict[str, Callable[[str, str], int]] = {
    "KMP": kmp_search,
    "Boyer-Moore": boyer_moore_search,
    "Rabin-Karp": rabin_karp_search,
}

PATTERNS = {
    "match":    "структури даних",
    "no_match": "рожевий поні",
}

REPEATS = 5
ITERATIONS = 1000


def measure(fn: Callable[[str, str], int], text: str, pattern: str) -> float:
    timer = timeit.Timer(lambda: fn(text, pattern))
    times = timer.repeat(repeat=REPEATS, number=ITERATIONS)
    return min(times) / ITERATIONS


def format_seconds(seconds: float) -> str:
    if seconds < 1e-6:
        return f"{seconds * 1e9:>9.2f} ns"
    if seconds < 1e-3:
        return f"{seconds * 1e6:>9.2f} µs"
    return f"{seconds * 1e3:>9.2f} ms"


def run() -> None:
    data_dir = Path(__file__).parent / "data"
    texts = {
        "article_1": (data_dir / "article_1.txt").read_text(encoding="utf-8"),
        "article_2": (data_dir / "article_2.txt").read_text(encoding="utf-8"),
    }

    print(f"{Fore.MAGENTA}Substring search benchmark — best of {REPEATS} (× {ITERATIONS} calls)\n")
    for name, text in texts.items():
        print(f"{Fore.MAGENTA}{name}: {len(text)} chars")
    print()
    for kind, pattern in PATTERNS.items():
        print(f"{Fore.MAGENTA}pattern [{kind}]: {pattern!r}")
    print()

    totals = dict.fromkeys(ALGORITHMS, 0.0)

    for text_name, text in texts.items():
        print(f"{Fore.CYAN}=== {text_name} ===")
        header = f"{'pattern':>10} | " + " | ".join(f"{name:>13}" for name in ALGORITHMS)
        print(header)
        print("-" * len(header))

        for kind, pattern in PATTERNS.items():
            row = [f"{kind:>10}"]
            cells: dict[str, float] = {}
            for algo_name, algo in ALGORITHMS.items():
                elapsed = measure(algo, text, pattern)
                cells[algo_name] = elapsed
                totals[algo_name] += elapsed
                row.append(f"{format_seconds(elapsed):>13}")
            winner = min(cells, key=cells.get)
            print(" | ".join(row) + f"  → {Fore.GREEN}{winner}{Fore.RESET}")
        print()

    print(f"{Fore.CYAN}=== overall (sum across both texts and both patterns) ===")
    for algo_name, total in sorted(totals.items(), key=lambda kv: kv[1]):
        print(f"  {algo_name:>13}: {format_seconds(total)}")
    overall_winner = min(totals, key=totals.get)
    print(f"\n{Fore.GREEN}Overall winner: {overall_winner}")


if __name__ == "__main__":
    run()
