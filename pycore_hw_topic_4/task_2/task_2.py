import random

def get_numbers_ticket(min, max, quantity) -> list:
    try:
        min_int = int(min)
        max_int = int(max)
        quantity_int = int(quantity)
    except (ValueError, TypeError):
        return []

    if (
        min_int < 1 or
        max_int > 1000 or
        min_int > max_int or
        quantity_int < 1 or
        quantity_int > (max_int - min_int + 1)
    ):
        return []

    numbers = random.sample(range(min_int, max_int + 1), quantity_int)
    return sorted(numbers)
