RK_BASE = 65537
RK_MOD = (1 << 61) - 1


def rabin_karp_search(text: str, pattern: str) -> int:
    if not pattern:
        return 0
    n, m = len(text), len(pattern)
    if m > n:
        return -1

    high = pow(RK_BASE, m - 1, RK_MOD)
    pattern_hash = 0
    text_hash = 0
    for i in range(m):
        pattern_hash = (pattern_hash * RK_BASE + ord(pattern[i])) % RK_MOD
        text_hash = (text_hash * RK_BASE + ord(text[i])) % RK_MOD

    for i in range(n - m + 1):
        if text_hash == pattern_hash and text[i:i + m] == pattern:
            return i
        if i < n - m:
            text_hash = (
                (text_hash - ord(text[i]) * high) * RK_BASE
                + ord(text[i + m])
            ) % RK_MOD
    return -1
