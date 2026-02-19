import re
from typing import Callable, Generator


def generator_numbers(text: str) -> Generator[float, None, None]:
    if not isinstance(text, str):
        raise TypeError("Text must be string")

    pattern = r"(?<!\S)[+-]?\d+(?:\.\d+)?(?!\S)"

    matches = re.finditer(pattern, text)

    for match in matches:
        yield float(match.group())


def sum_profit(text: str, func: Callable[[str], Generator[float, None, None]]) -> float:
    if not callable(func):
        raise TypeError("func must be callable")

    total = 0.0

    for number in func(text):
        total += number

    return total
