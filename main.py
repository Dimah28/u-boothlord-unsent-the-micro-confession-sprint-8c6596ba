#!/usr/bin/env python3
"""Unsent: The Micro-Confession Sprint — make.fun bounty.

Writes one two-part micro-confession (a To: line naming who it was
meant for, then the unsent message itself, one line written exactly as
it was typed) to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).
Python standard library only; deterministic: the same text every run.
"""

import os
import sys

# Gate: 1-260 characters, exactly 2 lines, no trailing newline.
MIN_CHARS = 1
MAX_CHARS = 260
MAX_MESSAGE_CHARS = 200

ENTRY_LINES = (
    "To: my older brother",
    "i still owe you the two hundred i borrowed for mum's medicine "
    "in 2019, and every payday i tell myself next month, because "
    "paying it back means admitting i spent three years pretending "
    "i forgot",
)


def build_entry() -> str:
    """Join the entry lines into the exact text that gets written."""
    return "\n".join(ENTRY_LINES)


def validate_entry(text: str) -> str:
    """Return the entry if it passes the gate, else fail loudly.

    Checks: non-blank, 1-260 characters, exactly two lines, first line
    a To: line, message line non-blank and at most 200 characters.
    Raises SystemExit with a clear message on any failure so a bad
    entry can never be written silently.
    """
    if not text.strip():
        raise SystemExit("invalid entry: entry must not be blank")
    if not MIN_CHARS <= len(text) <= MAX_CHARS:
        raise SystemExit(
            "invalid entry: entry must be %d-%d characters, got %d"
            % (MIN_CHARS, MAX_CHARS, len(text))
        )
    lines = text.split("\n")
    if len(lines) != 2:
        raise SystemExit(
            "invalid entry: entry must be exactly two lines "
            "(a To: line and one message line), got %d" % len(lines)
        )
    if not lines[0].startswith("To: "):
        raise SystemExit("invalid entry: first line must be a To: line")
    if not lines[1].strip():
        raise SystemExit("invalid entry: message line must not be blank")
    if len(lines[1]) > MAX_MESSAGE_CHARS:
        raise SystemExit(
            "invalid entry: message line must be at most %d characters, "
            "got %d" % (MAX_MESSAGE_CHARS, len(lines[1]))
        )
    return text


def write_entry(text: str, out_dir: str) -> str:
    """Write the validated entry to entry.txt; return the file path."""
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path


def main() -> int:
    text = validate_entry(build_entry())
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    write_entry(text, out_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
