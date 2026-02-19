import os
from colorama import Fore, init

from logs_task3 import (
    parse_log_line,
    load_logs,
    filter_logs_by_level,
    count_logs_by_level,
)

init(autoreset=True)


def run_tests():
    current_dir = os.path.dirname(__file__)
    test_file = os.path.join(current_dir, "data", "input.txt")

    # --- parse_log_line ---
    parsed = parse_log_line("2024-01-01 12:00:00 INFO System started")
    assert parsed["date"] == "2024-01-01"
    assert parsed["time"] == "12:00:00"
    assert parsed["level"] == "INFO"
    assert parsed["message"] == "System started"

    # lowercase level -> uppercase
    parsed = parse_log_line("2024-01-01 12:00:00 error Failure happened")
    assert parsed["level"] == "ERROR"

    # invalid format
    try:
        parse_log_line("invalid line")
        assert False
    except ValueError:
        pass

    # --- load_logs ---
    logs = load_logs(test_file)

    assert isinstance(logs, list)
    assert len(logs) > 0
    assert "level" in logs[0]

    # missing file
    try:
        load_logs("missing.txt")
        assert False
    except FileNotFoundError:
        pass

    # --- filter_logs_by_level ---
    info_logs = filter_logs_by_level(logs, "info")
    for log in info_logs:
        assert log["level"] == "INFO"

    # --- count_logs_by_level ---
    counts = count_logs_by_level(logs)

    assert isinstance(counts, dict)
    for level in counts.keys():
        assert level in ["INFO", "DEBUG", "ERROR", "WARNING"]

    print(f"{Fore.GREEN}All tests for logs task passed successfully!")


if __name__ == "__main__":
    run_tests()
