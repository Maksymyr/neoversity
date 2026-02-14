import sys
from pathlib import Path
from colorama import Fore, Style, init

init(autoreset=True)


def print_tree(path: Path, indent: str = ""):
    try:
        for item in sorted(path.iterdir()):
            if item.is_dir():
                print(f"{indent}{Fore.BLUE}{item.name}{Style.RESET_ALL}")
                print_tree(item, indent + "    ")
            else:
                print(f"{indent}{Fore.GREEN}{item.name}{Style.RESET_ALL}")
    except PermissionError:
        print(f"{indent}{Fore.RED}Permission denied{Style.RESET_ALL}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python dir_tree_cli.py <directory_path>")
        return

    path = Path(sys.argv[1])

    if not path.exists():
        print("Path does not exist")
        return

    if not path.is_dir():
        print("Path is not a directory")
        return

    print(f"{Fore.YELLOW}{path}{Style.RESET_ALL}")
    print_tree(path)


if __name__ == "__main__":
    main()
