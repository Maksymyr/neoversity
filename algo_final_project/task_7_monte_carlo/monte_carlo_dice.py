import argparse
import random
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt


THEORETICAL_PROBS = {
    2:  1 / 36,
    3:  2 / 36,
    4:  3 / 36,
    5:  4 / 36,
    6:  5 / 36,
    7:  6 / 36,
    8:  5 / 36,
    9:  4 / 36,
    10: 3 / 36,
    11: 2 / 36,
    12: 1 / 36,
}


def simulate(n_rolls: int, seed: int | None = None) -> Counter:
    """Roll two dice n_rolls times and return a Counter of sums."""
    rng = random.Random(seed)
    counts: Counter = Counter()
    for _ in range(n_rolls):
        s = rng.randint(1, 6) + rng.randint(1, 6)
        counts[s] += 1
    return counts


def empirical_probs(counts: Counter, n_rolls: int) -> dict[int, float]:
    return {s: counts.get(s, 0) / n_rolls for s in range(2, 13)}


def print_table(probs: dict[int, float], n_rolls: int) -> None:
    print(f"\nResults of {n_rolls:,} simulated rolls:\n")
    print(f"{'sum':>4} | {'simulated':>11} | {'theoretical':>13} | {'absolute err':>13} | {'relative err':>13}")
    print("-" * 64)
    for s in range(2, 13):
        sim = probs[s]
        theo = THEORETICAL_PROBS[s]
        abs_err = abs(sim - theo)
        rel_err = abs_err / theo if theo else 0
        print(
            f"{s:>4} | {sim * 100:>10.4f}% | {theo * 100:>12.4f}% | "
            f"{abs_err * 100:>12.4f}% | {rel_err * 100:>12.2f}%"
        )


def plot_distribution(probs: dict[int, float], n_rolls: int, save_to: Path | None = None) -> None:
    sums = list(range(2, 13))
    sim = [probs[s] * 100 for s in sums]
    theo = [THEORETICAL_PROBS[s] * 100 for s in sums]

    x = [s - 0.2 for s in sums]
    x2 = [s + 0.2 for s in sums]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(x, sim, width=0.4, label=f"Monte Carlo ({n_rolls:,} rolls)", color="#4A90D9", edgecolor="black")
    ax.bar(x2, theo, width=0.4, label="theoretical", color="#E67E22", edgecolor="black")
    ax.set_xticks(sums)
    ax.set_xlabel("sum of two dice")
    ax.set_ylabel("probability (%)")
    ax.set_title(f"Two-dice sum distribution: Monte Carlo vs theoretical")
    ax.legend()
    ax.grid(axis="y", linestyle=":", alpha=0.5)

    plt.tight_layout()
    if save_to is not None:
        plt.savefig(save_to, dpi=120)
        print(f"\nPlot saved to: {save_to}")
    else:
        plt.show()


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Monte Carlo simulation of two dice")
    p.add_argument("-n", "--rolls", type=int, default=100_000, help="number of rolls (default: 100,000)")
    p.add_argument("--seed", type=int, default=None, help="RNG seed (for reproducibility)")
    p.add_argument("--save", type=Path, default=None, help="save plot to file instead of showing")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    counts = simulate(args.rolls, seed=args.seed)
    probs = empirical_probs(counts, args.rolls)
    print_table(probs, args.rolls)
    plot_distribution(probs, args.rolls, save_to=args.save)


if __name__ == "__main__":
    main()
