from datetime import datetime, timedelta
from task_1 import get_days_from_today

def run_tests():
    today = datetime.today().date()
    today_str = today.strftime("%Y-%m-%d")

    # Correctness: Test with today's date should return 0
    assert get_days_from_today(today_str) == 0

    # Correctness: Test with date 10 days ago should return 10
    ten_days_ago = (today - timedelta(days=10)).strftime("%Y-%m-%d")
    assert get_days_from_today(ten_days_ago) == 10

    # Correctness: Test with date 5 days in the future should return -5
    five_days_later = (today + timedelta(days=5)).strftime("%Y-%m-%d")
    assert get_days_from_today(five_days_later) == -5

    # Correctness: Test with a fixed past date, check against manual calculation
    expected_diff = (today - datetime.strptime("2021-05-05", "%Y-%m-%d").date()).days
    assert get_days_from_today("2021-05-05") == expected_diff

    # Exception Handling: Test wrong format date string should raise ValueError
    try:
        get_days_from_today("05-05-2021")
        assert False, "Exception expected for wrong date format"
    except ValueError as e:
        assert str(e) == "Wrong date format. Please use 'YYYY-MM-DD'."

    # Exception Handling: Test invalid date (e.g. Feb 30) should raise ValueError
    try:
        get_days_from_today("2023-02-30")
        assert False, "Exception expected for invalid date"
    except ValueError as e:
        assert str(e) == "Wrong date format. Please use 'YYYY-MM-DD'."

    # If reached here, all tests passed successfully
    print("\033[92mAll tests for get_days_from_today passed successfully!\033[0m")

if __name__ == "__main__":
    run_tests()
