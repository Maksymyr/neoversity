from task_2 import get_numbers_ticket

def run_tests():
    # Valid input tests (correctness, uniqueness, sorted output)
    result = get_numbers_ticket(1, 49, 6)
    assert len(result) == 6  # Check quantity
    assert all(1 <= num <= 49 for num in result)  # Check range
    assert len(set(result)) == 6  # Check uniqueness
    assert result == sorted(result)  # Check sorted order

    result = get_numbers_ticket(10, 20, 1)
    assert len(result) == 1
    assert 10 <= result[0] <= 20

    result = get_numbers_ticket(5, 10, 6)
    assert result == [5, 6, 7, 8, 9, 10]

    # Invalid parameter values return empty list (validation)
    assert get_numbers_ticket(0, 10, 5) == []
    assert get_numbers_ticket(1, 1001, 5) == []
    assert get_numbers_ticket(1, 10, 11) == []
    assert get_numbers_ticket(20, 10, 5) == []
    assert get_numbers_ticket(1, 10, 0) == []

    # Type coercion: numeric strings accepted and converted correctly
    result = get_numbers_ticket("1", "49", "6")
    assert len(result) == 6
    assert all(1 <= num <= 49 for num in result)
    assert len(set(result)) == 6
    assert result == sorted(result)

    # Invalid types return empty list (error handling)
    assert get_numbers_ticket("abc", 49, 6) == []
    assert get_numbers_ticket(1, None, 6) == []
    assert get_numbers_ticket(1, 49, []) == []
    assert get_numbers_ticket({}, 49, 6) == []

    print("\033[92mAll tests for get_numbers_ticket passed successfully!\033[0m")

if __name__ == "__main__":
    run_tests()
