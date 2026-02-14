import os
from get_cats_info import get_cats_info
from colorama import Fore, init

init(autoreset=True)

def run_tests():
    current_dir = os.path.dirname(__file__)
    test_file = os.path.join(current_dir, "data", "input.txt")

    cats = get_cats_info(test_file)

    assert len(cats) == 5
    assert cats[0]["name"] == "Tayson"
    assert cats[1]["age"] == "1"

    try:
        get_cats_info("missing.txt")
        assert False
    except FileNotFoundError:
        pass

    print(f"{Fore.GREEN}All tests for get_cats_info passed successfully!")


if __name__ == "__main__":
    run_tests()
