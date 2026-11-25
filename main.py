#!/usr/bin/env python3
"""Unsent: The Micro-Confession Sprint — make.fun bounty.

Writes one two-part micro-confession (a To: line naming who it was
meant for, then the unsent message itself, one line written exactly as
it was typed) to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).
Python standard library only; deterministic: the same text every run.
"""

import os
import sys

ENTRY = (
    "To: my older brother\n"
    "i still owe you the two hundred i borrowed for mum's medicine "
    "in 2019, and every payday i tell myself next month, because "
    "paying it back means admitting i spent three years pretending "
    "i forgot"
)


def validate_entry(text: str) -> str:
    """Return the entry if it passes the gate, else raise ValueError."""
    if not text.strip():
        raise ValueError("entry must not be blank")
    if not 1 <= len(text) <= 260:
        raise ValueError("entry must be 1-260 characters, got %d" % len(text))
    lines = text.split("\n")
    if len(lines) != 2:
        raise ValueError("entry must be exactly two parts: a To: line and one message line")
    if not lines[0].startswith("To: "):
        raise ValueError("first line must be a To: line")
    if not lines[1].strip():
        raise ValueError("message line must not be blank")
    if len(lines[1]) > 200:
        raise ValueError("message line must be at most 200 characters, got %d" % len(lines[1]))
    return text


def main() -> int:
    try:
        text = validate_entry(ENTRY)
    except ValueError as exc:
        print("invalid entry: %s" % exc, file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.txt"), "w", encoding="utf-8") as f:
        f.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
