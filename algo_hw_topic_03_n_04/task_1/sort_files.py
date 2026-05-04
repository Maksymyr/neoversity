import argparse
import shutil
import sys
from pathlib import Path

from colorama import Fore, init

init(autoreset=True)

NO_EXT_DIR = "no_extension"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Recursively copy files from source into destination, "
                    "sorting them into sub-folders by file extension.",
    )
    parser.add_argument("source", type=Path, help="Path to the source directory")
    parser.add_argument(
        "destination",
        nargs="?",
        type=Path,
        default=Path("dist"),
        help="Path to the destination directory (default: dist)",
    )
    return parser.parse_args()


def copy_file(file_path: Path, destination: Path) -> None:
    extension = file_path.suffix.lstrip(".").lower() or NO_EXT_DIR
    target_dir = destination / extension
    try:
        target_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file_path, target_dir / file_path.name)
        print(f"{Fore.GREEN}copied: {file_path} -> {target_dir / file_path.name}")
    except OSError as exc:
        print(f"{Fore.RED}failed to copy {file_path}: {exc}")


def process_directory(source: Path, destination: Path) -> None:
    try:
        entries = list(source.iterdir())
    except OSError as exc:
        print(f"{Fore.RED}cannot read directory {source}: {exc}")
        return

    for entry in entries:
        try:
            if entry.is_symlink():
                print(f"{Fore.YELLOW}skip symlink: {entry}")
                continue
            if entry.resolve() == destination.resolve():
                print(f"{Fore.YELLOW}skip destination itself: {entry}")
                continue
            if entry.is_dir():
                process_directory(entry, destination)
            elif entry.is_file():
                copy_file(entry, destination)
        except OSError as exc:
            print(f"{Fore.RED}error processing {entry}: {exc}")


def main() -> int:
    args = parse_args()
    source: Path = args.source
    destination: Path = args.destination

    if not source.exists() or not source.is_dir():
        print(f"{Fore.RED}Source directory does not exist: {source}")
        return 1

    try:
        destination.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        print(f"{Fore.RED}Cannot create destination {destination}: {exc}")
        return 1

    if source.resolve() == destination.resolve():
        print(f"{Fore.RED}Source and destination must differ: {source}")
        return 1

    print(f"{Fore.MAGENTA}Sorting files: {source} -> {destination}")
    process_directory(source, destination)
    print(f"{Fore.MAGENTA}Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
