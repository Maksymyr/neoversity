from profit_utils import generator_numbers, sum_profit
from colorama import Fore, init

init(autoreset=True)


def run_tests():

    # Criterion: Correct extraction of real numbers
    text = "income 1000.01 bonus 27.45 extra 324.00"
    numbers = list(generator_numbers(text))
    assert numbers == [1000.01, 27.45, 324.0]

    # Criterion: Support integers
    text = "values 10 20 30"
    numbers = list(generator_numbers(text))
    assert numbers == [10.0, 20.0, 30.0]

    # Criterion: Support negative numbers
    text = "values -10 -20.5 +30"
    numbers = list(generator_numbers(text))
    assert numbers == [-10.0, -20.5, 30.0]

    # Criterion: Numbers must be separated by spaces
    text = "wrong100 wrong(200) wrong-300text"
    numbers = list(generator_numbers(text))
    assert numbers == []

    # Criterion: Correct sum calculation
    text = "profit 100.5 200.25 300"
    total = sum_profit(text, generator_numbers)
    assert total == 600.75

    # Criterion: Empty text → zero sum
    assert sum_profit("", generator_numbers) == 0.0

    # Criterion: Invalid text type → TypeError
    try:
        sum_profit(123, generator_numbers)
        assert False
    except TypeError:
        pass

    # Criterion: func must be callable
    try:
        sum_profit("100 200", "not a function")
        assert False
    except TypeError:
        pass

    print(f"{Fore.GREEN}All tests for generator_numbers and sum_profit passed successfully!")


if __name__ == "__main__":
    run_tests()
