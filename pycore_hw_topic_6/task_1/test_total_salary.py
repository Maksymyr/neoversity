import os
from total_salary import total_salary
from colorama import Fore, init

init(autoreset=True)

def run_tests():
    current_dir = os.path.dirname(__file__)
    test_file = os.path.join(current_dir, "data", "input.txt")

    total, avg = total_salary(test_file)

    assert total == 6000
    assert avg == 2000

    try:
        total_salary("missing.txt")
        assert False
    except FileNotFoundError:
        pass

    print(f"{Fore.GREEN}All tests for total_salary passed successfully!")


if __name__ == "__main__":
    run_tests()