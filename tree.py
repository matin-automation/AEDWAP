from pathlib import Path

ROOT = Path(__file__).parent
OUTPUT = ROOT / "tree.txt"

EXCLUDED_DIRS = {
    ".git",
    "venv",
    ".venv",
    "__pycache__",
}

EXCLUDED_FILES = {
    ".env",
    "tree.txt",
}


def should_exclude(path: Path) -> bool:
    if path.name in EXCLUDED_DIRS:
        return True

    if path.name in EXCLUDED_FILES:
        return True

    if path.is_file() and path.suffix == ".pyc":
        return True

    return False


def build_tree(path: Path, prefix: str = ""):
    entries = [
        entry
        for entry in path.iterdir()
        if not should_exclude(entry)
    ]

    entries.sort(
        key=lambda entry: (
            entry.is_file(),
            entry.name.lower()
        )
    )

    for index, entry in enumerate(entries):
        is_last = index == len(entries) - 1

        connector = "└── " if is_last else "├── "
        print(f"{prefix}{connector}{entry.name}")

        if entry.is_dir():
            extension = "    " if is_last else "│   "
            build_tree(entry, prefix + extension)


print(ROOT.name)

# Capture output while also writing it
import io
import sys

buffer = io.StringIO()
original_stdout = sys.stdout
sys.stdout = buffer

print(ROOT.name)
build_tree(ROOT)

sys.stdout = original_stdout

OUTPUT.write_text(buffer.getvalue(), encoding="utf-8")

print(f"Tree written to: {OUTPUT}")