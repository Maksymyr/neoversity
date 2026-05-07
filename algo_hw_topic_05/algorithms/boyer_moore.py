def boyer_moore_search(text: str, pattern: str) -> int:
    if not pattern:
        return 0
    n, m = len(text), len(pattern)
    if m > n:
        return -1

    bad_char = {ch: idx for idx, ch in enumerate(pattern)}
    s = 0
    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        if j < 0:
            return s
        shift = j - bad_char.get(text[s + j], -1)
        s += max(1, shift)
    return -1
