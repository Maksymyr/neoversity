import argparse
import turtle


def koch_segment(t: turtle.Turtle, length: float, level: int) -> None:
    if level == 0:
        t.forward(length)
        return

    sub = length / 3
    koch_segment(t, sub, level - 1)
    t.left(60)
    koch_segment(t, sub, level - 1)
    t.right(120)
    koch_segment(t, sub, level - 1)
    t.left(60)
    koch_segment(t, sub, level - 1)


def draw_snowflake(level: int, size: float = 300.0) -> None:
    screen = turtle.Screen()
    screen.title(f"Koch snowflake — level {level}")
    screen.bgcolor("white")

    t = turtle.Turtle()
    t.speed(0)
    t.color("steelblue")
    t.penup()
    t.goto(-size / 2, size / 3)
    t.pendown()

    for _ in range(3):
        koch_segment(t, size, level)
        t.right(120)

    t.hideturtle()
    screen.mainloop()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Draw Koch snowflake fractal")
    parser.add_argument(
        "level",
        nargs="?",
        type=int,
        default=None,
        help="Recursion level (>= 0). If omitted, prompts interactively.",
    )
    parser.add_argument(
        "--size",
        type=float,
        default=300.0,
        help="Side length of the base triangle (default: 300)",
    )
    return parser.parse_args()


SOFT_CAP = 7


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
            f"Level {level} > {SOFT_CAP} may take a long time and produce "
            f"sub-pixel detail. Continue? [y/N]: "
        ).strip().lower()
        if answer not in ("y", "yes"):
            print("Aborted.")
            return

    draw_snowflake(level, args.size)


if __name__ == "__main__":
    main()
