from caching_fibonacci import caching_fibonacci
from colorama import Fore, init

init(autoreset=True)


def run_tests():
    fib = caching_fibonacci()

    # Criterion: Correct Fibonacci calculation
    assert fib(0) == 0
    assert fib(-5) == 0
    assert fib(1) == 1
    assert fib(10) == 55
    assert fib(15) == 610

    # Criterion: Cache reuse (second call should still be correct)
    assert fib(15) == 610

    # Criterion: Accept convertible values
    assert fib("10") == 55
    assert fib(10.0) == 55

    # Criterion: Invalid non-numeric input → TypeError
    try:
        fib("abc")
        assert False
    except TypeError:
        pass

    print(f"{Fore.GREEN}All tests for caching_fibonacci passed successfully!")


if __name__ == "__main__":
    run_tests()
