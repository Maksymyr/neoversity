import re

def normalize_phone(phone_number: str) -> str:
    cleaned = re.sub(r"[^\d+]", "", phone_number.strip())

    if cleaned.startswith("+"):
        digits = "+" + re.sub(r"\D", "", cleaned)
    else:
        digits_only = re.sub(r"\D", "", cleaned)

        if digits_only.startswith("380"):
            digits = "+" + digits_only
        else:
            digits = "+38" + digits_only

    digits_only_part = digits.lstrip("+")
    if len(digits_only_part) < 9 or len(digits_only_part) > 15:
        raise ValueError(f"Invalid phone number length: {digits}")

    return digits