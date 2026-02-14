def total_salary(path: str) -> tuple[int, float]:
    total = 0
    count = 0

    try:
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                try:
                    fullname, salary = line.split(",")
                    total += int(salary)
                    count += 1
                except ValueError:
                    raise ValueError("Invalid file data format. Expected: 'Fullname,Salary'")

        if count == 0:
            return 0, 0.0

        return total, total / count

    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}")
