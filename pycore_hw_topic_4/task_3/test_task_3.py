from task_3 import normalize_phone

def run_tests():
    # Correctness: input with various formats and expected normalized output
    inputs = [
        "+38(050)123-32-34",
        "0503451234",
        "(050)8889900",
        "38050-111-22-22",
        "38050 111 22 11",
        "067\t123 4567",
        "(095) 234-5678\n",
        "+380 44 123 4567",
        "  +38(050)123-32-34  ",
    ]
    expected = [
        "+380501233234",
        "+380503451234",
        "+380508889900",
        "+380501112222",
        "+380501112211",
        "+380671234567",
        "+380952345678",
        "+380441234567",
        "+380501233234",
    ]

    for i, phone in enumerate(inputs):
        assert normalize_phone(phone) == expected[i], f"Failed on input: {phone}"

    # Exception Handling: invalid strings should raise ValueError
    invalid_inputs = [
        "abc",
        "+123",
        "12",
        "",
        "+",
        "+3801234",  # too short
        "12345678901234567890",  # too long
    ]

    for invalid in invalid_inputs:
        try:
            normalize_phone(invalid)
            assert False, f"Expected ValueError for invalid input: {invalid}"
        except ValueError:
            pass

    print("\033[92mmAll tests for normalize_phone passed successfully!\033[0m")

if __name__ == "__main__":
    run_tests()