import sys
from collections import Counter


def parse_log_line(line: str) -> dict:
    parts = line.strip().split(" ", 3)
    if len(parts) < 4:
        raise ValueError("Invalid log line format")

    date, time, level, message = parts
    return {
        "date": date,
        "time": time,
        "level": level.upper(),
        "message": message,
    }


def load_logs(file_path: str) -> list:
    logs = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                if not line.strip():
                    continue
                logs.append(parse_log_line(line))
    except FileNotFoundError:
        raise FileNotFoundError(f"Log file not found: {file_path}")

    return logs


def filter_logs_by_level(logs: list, level: str) -> list:
    level = level.upper()
    return list(filter(lambda log: log["level"] == level, logs))


def count_logs_by_level(logs: list) -> dict:
    return dict(Counter(log["level"] for log in logs))


def display_log_counts(counts: dict):
    print("Log Level      | Count")
    print("----------------|-------")

    for level in ["INFO", "DEBUG", "ERROR", "WARNING"]:
        print(f"{level:<14} | {counts.get(level, 0)}")


def display_log_details(logs: list, level: str):
    print(f"\nDetails for log level '{level.upper()}':")

    for log in logs:
        print(f"{log['date']} {log['time']} - {log['message']}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <log_file_path> [log_level]")
        sys.exit(1)

    file_path = sys.argv[1]
    level_filter = sys.argv[2] if len(sys.argv) > 2 else None

    logs = load_logs(file_path)
    counts = count_logs_by_level(logs)

    display_log_counts(counts)

    if level_filter:
        filtered_logs = filter_logs_by_level(logs, level_filter)
        display_log_details(filtered_logs, level_filter)


if __name__ == "__main__":
    main()
