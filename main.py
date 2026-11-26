"""One-line meeting killer.

A single sentence that could have replaced an entire pointless meeting,
with no context and no explanation. This program checks the line against
the bounty gate (1-200 characters, one line, not only whitespace), writes
it to $MAKEFUN_OUTPUT_DIR/entry.txt with no trailing newline, and reports
where it landed plus its SHA-256.
"""

import hashlib
import io
import os
from pathlib import Path

ONE_LINER = "This could have been an email, but then nobody would have felt important for 45 minutes."


def scrutinize(line):
    """Reject any line that fails the bounty gate."""
    if not isinstance(line, str):
        raise ValueError("line must be text")
    if not 1 <= len(line) <= 200:
        raise ValueError("line must be 1-200 characters")
    if not line.strip():
        raise ValueError("line must not be only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    return line


def dest_dir():
    """Find the output folder from the environment."""
    return Path(os.getenv("MAKEFUN_OUTPUT_DIR", "output"))


def scribe(folder, line):
    """Write the line to entry.txt with the io module."""
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / "entry.txt"
    payload = line.encode("utf-8")
    with io.open(target, "w", encoding="utf-8") as handle:
        handle.write(line)
    return target, payload


def doublecheck(target, line):
    """Read entry.txt back and confirm it matches the line."""
    with io.open(target, "r", encoding="utf-8") as handle:
        stored = handle.read()
    assert stored == line, "entry.txt differs from the line"
    assert stored.encode("utf-8") == line.encode("utf-8"), "bytes differ"
    assert stored == stored.rstrip(), "trailing whitespace found"
    return stored


def launch_it():
    """Validate the line, write it, verify it, and report the result."""
    scrutinize(ONE_LINER)
    folder = dest_dir()
    target, payload = scribe(folder, ONE_LINER)
    doublecheck(target, ONE_LINER)
    digest = hashlib.sha256(payload).hexdigest()
    print("entry:", target, "|", len(payload), "bytes |", digest)


if __name__ == "__main__":
    launch_it()
