import argparse
import math

import matplotlib.pyplot as plt
from matplotlib.axes import Axes


def draw_branch(
    ax: Axes,
    x: float,
    y: float,
    length: float,
    angle: float,
    depth: int,
    angle_delta: float,
    length_ratio: float,
    color: str,
) -> None:
    if depth == 0 or length < 0.5:
        return

    x_end = x + length * math.cos(angle)
    y_end = y + length * math.sin(angle)

    linewidth = max(0.5, depth * 0.4)
    ax.plot([x, x_end], [y, y_end], color=color, linewidth=linewidth, solid_capstyle="round")

    new_length = length * length_ratio
    draw_branch(ax, x_end, y_end, new_length, angle + angle_delta, depth - 1, angle_delta, length_ratio, color)
    draw_branch(ax, x_end, y_end, new_length, angle - angle_delta, depth - 1, angle_delta, length_ratio, color)


def draw_pythagoras_tree(
    level: int,
    trunk_length: float = 100.0,
    angle_delta_deg: float = 45.0,
    length_ratio: float = 0.7,
    color: str = "#A52A2A",
) -> None:
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(f"Pythagoras tree — level {level}")

    draw_branch(
        ax=ax,
        x=0,
        y=0,
        length=trunk_length,
        angle=math.pi / 2,  # straight up
        depth=level,
        angle_delta=math.radians(angle_delta_deg),
        length_ratio=length_ratio,
        color=color,
    )

    plt.tight_layout()
    plt.show()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Draw a Pythagoras tree fractal")
    parser.add_argument(
        "level",
        nargs="?",
        type=int,
        default=None,
        help="Recursion depth (>= 0). If omitted, prompts interactively.",
    )
    parser.add_argument("--angle", type=float, default=45.0, help="Branch angle in degrees (default: 45)")
    parser.add_argument("--ratio", type=float, default=0.7, help="Length ratio child/parent (default: 0.7)")
    parser.add_argument("--trunk", type=float, default=100.0, help="Trunk length (default: 100)")
    return parser.parse_args()


SOFT_CAP = 12


def main() -> None:
    args = parse_args()
    level = args.level
    if level is None:
        try:
            level = int(input(f"Enter recursion level (0..{SOFT_CAP} recommended): "))
        except ValueError:
            print("Recursion level must be an integer.")
            return

    if level < 0:
        print("Recursion level must be >= 0.")
        return

    if level > SOFT_CAP:
        answer = input(
            f"Level {level} > {SOFT_CAP} will produce 2^{level} branches and may be slow. "
            f"Continue? [y/N]: "
        ).strip().lower()
        if answer not in ("y", "yes"):
            print("Aborted.")
            return

    draw_pythagoras_tree(
        level=level,
        trunk_length=args.trunk,
        angle_delta_deg=args.angle,
        length_ratio=args.ratio,
    )


if __name__ == "__main__":
    main()
