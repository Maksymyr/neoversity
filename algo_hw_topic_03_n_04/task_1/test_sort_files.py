import tempfile
from pathlib import Path

from sort_files import process_directory, NO_EXT_DIR


def make_tree(root: Path) -> None:
    (root / "sub1" / "sub2").mkdir(parents=True)
    (root / "a.txt").write_text("a")
    (root / "b.JPG").write_bytes(b"b")
    (root / "sub1" / "c.pdf").write_bytes(b"c")
    (root / "sub1" / "sub2" / "d.txt").write_text("d")
    (root / "sub1" / "sub2" / "no_ext").write_text("e")


def run_tests() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        src = root / "src"
        dst = root / "dist"
        src.mkdir()
        make_tree(src)

        dst.mkdir()
        process_directory(src, dst)

        assert (dst / "txt" / "a.txt").is_file()
        assert (dst / "txt" / "d.txt").is_file()
        assert (dst / "jpg" / "b.JPG").is_file()
        assert (dst / "pdf" / "c.pdf").is_file()
        assert (dst / NO_EXT_DIR / "no_ext").is_file()

        assert (dst / "txt" / "a.txt").read_text() == "a"
        assert (dst / "pdf" / "c.pdf").read_bytes() == b"c"

        copied = sorted(p.relative_to(dst).as_posix() for p in dst.rglob("*") if p.is_file())
        assert copied == sorted([
            "jpg/b.JPG",
            f"{NO_EXT_DIR}/no_ext",
            "pdf/c.pdf",
            "txt/a.txt",
            "txt/d.txt",
        ])

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        src = root / "src"
        dst = root / "src" / "dist"
        src.mkdir()
        (src / "x.txt").write_text("x")
        dst.mkdir()
        process_directory(src, dst)
        assert (dst / "txt" / "x.txt").is_file()
        nested = list((dst / "dist").rglob("*")) if (dst / "dist").exists() else []
        assert nested == []

    print("All tests passed!")


if __name__ == "__main__":
    run_tests()
