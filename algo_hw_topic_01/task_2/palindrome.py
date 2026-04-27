from collections import deque

from colorama import Fore, init

init(autoreset=True)


def is_palindrome(text: str) -> bool:
    normalized = "".join(ch for ch in text.lower() if not ch.isspace())
    chars: deque[str] = deque(normalized)

    while len(chars) > 1:
        if chars.popleft() != chars.pop():
            return False
    return True


def main() -> None:
    print(f"{Fore.MAGENTA}Palindrome checker (empty input to quit)")
    while True:
        text = input(f"{Fore.GREEN}> text: ")
        if not text:
            print(f"{Fore.MAGENTA}Bye!")
            break

        if is_palindrome(text):
            print(f"{Fore.CYAN}'{text}' is a palindrome")
        else:
            print(f"{Fore.YELLOW}'{text}' is NOT a palindrome")


if __name__ == "__main__":
    main()
