import math
from unittest.mock import MagicMock

from pythagoras_tree import draw_branch


def count_lines(level: int) -> int:
    """A binary fractal tree at depth n has 2^(n+1) - 1 line segments
    (trunk + branches at every level)."""
    ax = MagicMock()
    calls = {"count": 0}

    def plot(*_args, **_kwargs):
        calls["count"] += 1

    ax.plot.side_effect = plot
    draw_branch(
        ax=ax,
        x=0.0,
        y=0.0,
        length=100.0,
        angle=math.pi / 2,
        depth=level,
        angle_delta=math.radians(45),
        length_ratio=0.7,
        color="red",
    )
    return calls["count"]


def total_length(level: int, trunk: float, ratio: float) -> float:
    """Total length = trunk * sum(2^k * ratio^k) for k in 0..level-1 = trunk * (1-(2r)^level)/(1-2r)
    when 2r != 1."""
    ax = MagicMock()
    total = {"v": 0.0}

    def plot(x_pair, y_pair, **_):
        dx = x_pair[1] - x_pair[0]
        dy = y_pair[1] - y_pair[0]
        total["v"] += math.hypot(dx, dy)

    ax.plot.side_effect = plot
    draw_branch(
        ax=ax,
        x=0.0,
        y=0.0,
        length=trunk,
        angle=math.pi / 2,
        depth=level,
        angle_delta=math.radians(45),
        length_ratio=ratio,
        color="red",
    )
    return total["v"]


def run_tests() -> None:
    # depth 0 should draw nothing
    assert count_lines(0) == 0

    # depth 1 = trunk only = 1 line
    assert count_lines(1) == 1

    # depth n = 1 + 2 + 4 + ... + 2^(n-1) = 2^n - 1
    for level in range(1, 7):
        assert count_lines(level) == (1 << level) - 1, (level, count_lines(level))

    # total length geometric series check
    trunk = 100.0
    ratio = 0.5
    for level in range(1, 6):
        # sum_{k=0}^{level-1} 2^k * r^k * trunk = trunk * ((2r)^level - 1) / (2r - 1) when 2r != 1
        # for r = 0.5, 2r = 1, so total = trunk * level
        expected = trunk * level
        actual = total_length(level, trunk, ratio)
        assert abs(actual - expected) < 1e-6, (level, actual, expected)

    print("All tests passed!")


if __name__ == "__main__":
    run_tests()
