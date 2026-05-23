import argparse
from pathlib import Path
from typing import Callable

import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as spi


def f(x):
    return x ** 2


def monte_carlo_mean(fn: Callable[[float], float], a: float, b: float, n: int, seed: int | None = None) -> float:
    """Mean-value Monte Carlo: I ≈ (b - a) · mean(f(x_i)), x_i ~ Uniform(a, b)."""
    rng = np.random.default_rng(seed)
    xs = rng.uniform(a, b, size=n)
    return float((b - a) * np.mean(fn(xs)))


def monte_carlo_hit_miss(
    fn: Callable[[float], float],
    a: float,
    b: float,
    y_max: float,
    n: int,
    seed: int | None = None,
) -> float:
    """Hit-or-miss Monte Carlo: sample (x, y) in rectangle, count those under f(x).
    Assumes f(x) ≥ 0 on [a, b] and f(x) ≤ y_max."""
    rng = np.random.default_rng(seed)
    xs = rng.uniform(a, b, size=n)
    ys = rng.uniform(0, y_max, size=n)
    hits = int(np.sum(ys <= fn(xs)))
    return float((b - a) * y_max * hits / n)


def plot_function(fn, a: float, b: float, save_to: Path | None = None) -> None:
    x = np.linspace(a - 0.5, b + 0.5, 400)
    y = fn(x)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x, y, "r", linewidth=2)

    ix = np.linspace(a, b)
    iy = fn(ix)
    ax.fill_between(ix, iy, color="gray", alpha=0.3)

    ax.set_xlim([x[0], x[-1]])
    ax.set_ylim([min(0, float(y.min())), float(y.max()) + 0.1])
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.axvline(x=a, color="gray", linestyle="--")
    ax.axvline(x=b, color="gray", linestyle="--")
    ax.set_title(f"Графік інтегрування f(x) = x^2 від {a} до {b}")
    ax.grid(True)

    plt.tight_layout()
    if save_to is not None:
        plt.savefig(save_to, dpi=120)
        print(f"function plot saved to: {save_to}")
    else:
        plt.show()


def plot_convergence(fn, a: float, b: float, exact: float, sample_sizes: list[int], seed: int = 42, save_to: Path | None = None) -> None:
    estimates_mean = []
    estimates_hm = []
    errors_mean = []
    errors_hm = []
    y_max = float(np.max(fn(np.linspace(a, b, 1000))))

    for n in sample_sizes:
        m = monte_carlo_mean(fn, a, b, n, seed=seed)
        hm = monte_carlo_hit_miss(fn, a, b, y_max, n, seed=seed)
        estimates_mean.append(m)
        estimates_hm.append(hm)
        errors_mean.append(abs(m - exact))
        errors_hm.append(abs(hm - exact))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    ax1.axhline(y=exact, color="green", linestyle="--", label=f"exact = {exact:.6f}")
    ax1.plot(sample_sizes, estimates_mean, "o-", label="mean-value MC", color="#4A90D9")
    ax1.plot(sample_sizes, estimates_hm, "s-", label="hit-or-miss MC", color="#E67E22")
    ax1.set_xscale("log")
    ax1.set_xlabel("N (number of samples)")
    ax1.set_ylabel("estimated integral")
    ax1.set_title("MC estimate vs N")
    ax1.legend()
    ax1.grid(True, alpha=0.4)

    ax2.loglog(sample_sizes, errors_mean, "o-", label="mean-value MC", color="#4A90D9")
    ax2.loglog(sample_sizes, errors_hm, "s-", label="hit-or-miss MC", color="#E67E22")
    # theoretical 1/sqrt(N) reference
    ref = [errors_mean[0] * (sample_sizes[0] / n) ** 0.5 for n in sample_sizes]
    ax2.loglog(sample_sizes, ref, "k:", label=r"$O(1/\sqrt{N})$ reference", alpha=0.6)
    ax2.set_xlabel("N (number of samples)")
    ax2.set_ylabel("|error|")
    ax2.set_title("Absolute error vs N")
    ax2.legend()
    ax2.grid(True, alpha=0.4, which="both")

    plt.tight_layout()
    if save_to is not None:
        plt.savefig(save_to, dpi=120)
        print(f"convergence plot saved to: {save_to}")
    else:
        plt.show()


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Monte Carlo numerical integration")
    p.add_argument("-a", type=float, default=0.0, help="lower bound (default: 0)")
    p.add_argument("-b", type=float, default=2.0, help="upper bound (default: 2)")
    p.add_argument("-n", "--samples", type=int, default=1_000_000, help="number of samples (default: 1,000,000)")
    p.add_argument("--seed", type=int, default=42, help="RNG seed")
    p.add_argument("--save", action="store_true", help="save plots to files instead of showing")
    return p.parse_args()


def main() -> None:
    args = parse_args()

    exact_analytical = (args.b ** 3 - args.a ** 3) / 3  # ∫ x^2 dx = x^3/3
    quad_value, quad_err = spi.quad(f, args.a, args.b)

    y_max = float(max(f(args.a), f(args.b)))
    mc_mean = monte_carlo_mean(f, args.a, args.b, args.samples, seed=args.seed)
    mc_hm = monte_carlo_hit_miss(f, args.a, args.b, y_max, args.samples, seed=args.seed)

    print(f"\nFunction: f(x) = x^2")
    print(f"Interval: [{args.a}, {args.b}]")
    print(f"Samples:  {args.samples:,}\n")
    print(f"{'method':>22} | {'value':>15} | {'abs error':>15} | {'rel error':>10}")
    print("-" * 72)
    print(f"{'analytical (x^3/3)':>22} | {exact_analytical:>15.10f} | {'(reference)':>15} | {'—':>10}")
    print(f"{'scipy.quad':>22} | {quad_value:>15.10f} | {abs(quad_value - exact_analytical):>15.2e} | {abs(quad_value - exact_analytical) / exact_analytical * 100:>9.4f}%")
    print(f"{'Monte Carlo mean':>22} | {mc_mean:>15.10f} | {abs(mc_mean - exact_analytical):>15.2e} | {abs(mc_mean - exact_analytical) / exact_analytical * 100:>9.4f}%")
    print(f"{'Monte Carlo hit/miss':>22} | {mc_hm:>15.10f} | {abs(mc_hm - exact_analytical):>15.2e} | {abs(mc_hm - exact_analytical) / exact_analytical * 100:>9.4f}%")

    base = Path(__file__).parent
    plot_function(f, args.a, args.b, save_to=base / "integration_area.png" if args.save else None)
    plot_convergence(
        f, args.a, args.b, exact_analytical,
        sample_sizes=[100, 1_000, 10_000, 100_000, 1_000_000],
        seed=args.seed,
        save_to=base / "convergence.png" if args.save else None,
    )


if __name__ == "__main__":
    main()
