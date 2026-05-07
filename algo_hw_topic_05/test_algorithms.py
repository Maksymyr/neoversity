from pathlib import Path

from algorithms import boyer_moore_search, kmp_search, rabin_karp_search

ALGORITHMS = (kmp_search, boyer_moore_search, rabin_karp_search)


def run_tests() -> None:
    for algorithm in ALGORITHMS:
        assert algorithm("", "") == 0
        assert algorithm("abc", "") == 0
        assert algorithm("", "abc") == -1
        assert algorithm("abc", "abcd") == -1

        assert algorithm("abcdef", "abc") == 0
        assert algorithm("abcdef", "def") == 3
        assert algorithm("abcdef", "cde") == 2
        assert algorithm("abcdef", "xyz") == -1

        assert algorithm("aaaa", "aa") == 0
        assert algorithm("aaab", "aab") == 1

        assert algorithm("ababcabab", "abab") == 0
        assert algorithm("xababcababy", "abab") == 1

        assert algorithm("Hello, world!", "world") == 7
        assert algorithm("Hello, world!", "World") == -1

        text = "алгоритм пошуку — це алгоритм"
        assert algorithm(text, "алгоритм") == 0
        assert algorithm(text, "пошуку") == 9
        assert algorithm(text, "немає") == -1

        long_text = "ab" * 1000 + "needle" + "cd" * 1000
        assert algorithm(long_text, "needle") == 2000

    data_dir = Path(__file__).parent / "data"
    article_1 = (data_dir / "article_1.txt").read_text(encoding="utf-8")
    article_2 = (data_dir / "article_2.txt").read_text(encoding="utf-8")

    for algorithm in ALGORITHMS:
        assert algorithm(article_1, "алгоритм") == article_1.find("алгоритм")
        assert algorithm(article_1, "рожевий поні") == -1

        assert algorithm(article_2, "B+-дерево") == article_2.find("B+-дерево")
        assert algorithm(article_2, "рожевий поні") == -1

    print("All tests passed!")


if __name__ == "__main__":
    run_tests()
