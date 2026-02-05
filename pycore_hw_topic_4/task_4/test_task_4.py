from datetime import datetime, timedelta
from task_4 import get_upcoming_birthdays

def next_weekend(start_date, weekday_target):
    days_ahead = weekday_target - start_date.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return start_date + timedelta(days=days_ahead)

def run_tests():
    today = datetime.today().date()

    saturday = next_weekend(today, 5)
    sunday = next_weekend(today, 6)

    users = [
        {"name": "Alice", "birthday": today.strftime("1990.%m.%d")},                          # Birthday today
        {"name": "Bob", "birthday": (today + timedelta(days=3)).strftime("1985.%m.%d")},      # Birthday in 3 days
        {"name": "Charlie", "birthday": (today + timedelta(days=7)).strftime("1975.%m.%d")},  # Birthday in 7 days
        {"name": "Dave", "birthday": saturday.strftime("2000.%m.%d")},                        # Birthday on Saturday
        {"name": "Eve", "birthday": sunday.strftime("1995.%m.%d")},                           # Birthday on Sunday
        {"name": "Frank", "birthday": (today + timedelta(days=8)).strftime("1999.%m.%d")},    # Birthday in 8 days (excluded)
        {"name": "Grace", "birthday": (today + timedelta(days=2)).strftime("1988.%m.%d")},    # Birthday in 2 days
    ]

    results = get_upcoming_birthdays(users)
    names = [user["name"] for user in results]

    # Criterion: Correctness of birthday selection within 7 days (including boundary)
    assert "Frank" not in names, "User with birthday 8 days ahead should not be included"
    assert "Alice" in names
    assert "Bob" in names
    assert "Charlie" in names
    assert "Dave" in names
    assert "Eve" in names
    assert "Grace" in names

    # Criterion: Weekend birthdays shifted to Monday
    for user in results:
        if user["name"] in ("Dave", "Eve"):
            cong_date = datetime.strptime(user["congratulation_date"], "%Y.%m.%d").date()
            assert cong_date.weekday() == 0, f"Birthday for {user['name']} should be moved to Monday"

    # Criterion: Structured output & date format correctness
    for user in results:
        assert "name" in user and "congratulation_date" in user
        try:
            datetime.strptime(user["congratulation_date"], "%Y.%m.%d")
        except ValueError:
            assert False, f"congratulation_date format incorrect for user {user['name']}"

    # User missing 'birthday' key
    users_missing_birthday = [{"name": "NoBirthday"}]
    result = get_upcoming_birthdays(users_missing_birthday)
    # Criterion: Function handles missing keys without crashing (error handling)
    assert result == [], "Users with missing 'birthday' key should be skipped"

    # User missing 'name' key but valid birthday
    users_missing_name = [{"birthday": datetime.today().strftime("%Y.%m.%d")}]
    result = get_upcoming_birthdays(users_missing_name)
    assert result == [], "Users with missing 'name' key should be skipped"

    # User with invalid birthday format
    users_invalid_format = [{"name": "InvalidDate", "birthday": "31-12-2020"}]
    result = get_upcoming_birthdays(users_invalid_format)
    assert result == [], "Users with invalid birthday format should be skipped"

    # Mixed valid and invalid users
    users_mixed = [
        {"name": "ValidUser", "birthday": datetime.today().strftime("1990.%m.%d")},
        {"name": "InvalidUser", "birthday": "wrong-format"},
        {"name": "NoBirthdayKey"},
    ]
    result = get_upcoming_birthdays(users_mixed)
    names = [user["name"] for user in result]
    assert "ValidUser" in names, "Valid user should appear"
    assert all(name != "InvalidUser" for name in names), "Invalid user should be skipped"
    assert all(name != "NoBirthdayKey" for name in names), "User missing birthday should be skipped"

    print("\033[92mmAll tests for get_upcoming_birthdays passed successfully!\033[0m")

if __name__ == "__main__":
    run_tests()
