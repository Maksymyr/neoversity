def kmp_search(text: str, pattern: str) -> int:
    if not pattern:
        return 0
    n, m = len(text), len(pattern)
    if m > n:
        return -1

    lps = _compute_lps(pattern)
    i = j = 0
    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == m:
                return i - m
        elif j > 0:
            j = lps[j - 1]
        else:
            i += 1
    return -1


def _compute_lps(pattern: str) -> list[int]:
    m = len(pattern)
    lps = [0] * m
    length = 0
    i = 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length > 0:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1
    return lps
