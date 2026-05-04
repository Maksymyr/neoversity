from unittest.mock import MagicMock

from koch_snowflake import koch_segment


def count_segments(level: int) -> int:
    """A Koch curve at level n has 4**n straight segments."""
    t = MagicMock()
    state = {"forward_calls": 0}

    def forward(_length):
        state["forward_calls"] += 1

    t.forward.side_effect = forward
    koch_segment(t, length=81.0, level=level)
    return state["forward_calls"]


def total_length(level: int, base_length: float) -> float:
    t = MagicMock()
    total = {"value": 0.0}

    def forward(length):
        total["value"] += length

    t.forward.side_effect = forward
    koch_segment(t, length=base_length, level=level)
    return total["value"]


def run_tests() -> None:
    assert count_segments(0) == 1
    assert count_segments(1) == 4
    assert count_segments(2) == 16
    assert count_segments(3) == 64

    base = 81.0
    for level in range(5):
        expected = base * (4 / 3) ** level
        actual = total_length(level, base)
        assert abs(actual - expected) < 1e-9, (level, actual, expected)

    print("All tests passed!")


if __name__ == "__main__":
    run_tests()
