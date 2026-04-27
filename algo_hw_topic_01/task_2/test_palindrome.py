from palindrome import is_palindrome


def run_tests() -> None:
    assert is_palindrome("kayak") is True
    assert is_palindrome("level") is True
    assert is_palindrome("racecar") is True

    assert is_palindrome("hello") is False
    assert is_palindrome("python") is False

    assert is_palindrome("Kayak") is True
    assert is_palindrome("RaceCar") is True

    assert is_palindrome("nurses run") is True
    assert is_palindrome("A man a plan a canal Panama") is True
    assert is_palindrome("Was it a car or a cat I saw") is True

    assert is_palindrome("a") is True
    assert is_palindrome("") is True
    assert is_palindrome("ab") is False
    assert is_palindrome("aa") is True

    print("All tests passed!")


if __name__ == "__main__":
    run_tests()
