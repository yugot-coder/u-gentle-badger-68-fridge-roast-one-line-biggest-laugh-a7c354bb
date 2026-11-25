"""Fridge Roast: One Line, Biggest Laugh.

Writes a single roast line for a smart fridge to /output/entry.txt.

Standard library only. Deterministic: the same entry text is written
on every run.
"""

import hashlib
import os

ENTRY = (
    'I asked my fridge for a snack and it said "based on your recent '
    'choices" \u2014 my appliance is fat-shaming me with analytics.'
)

OUTPUT_PATH = "/output/entry.txt"

MIN_LENGTH = 1
MAX_LENGTH = 200


def validate_entry(text):
    """Check the entry against the competition gate.

    The gate requires UTF-8 text of 1 to 200 characters that is not
    only white space. Raises ValueError on any violation.
    """
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    text.encode("utf-8")  # raises UnicodeEncodeError if not valid UTF-8
    if not MIN_LENGTH <= len(text) <= MAX_LENGTH:
        raise ValueError(
            "entry must be %d to %d characters, got %d"
            % (MIN_LENGTH, MAX_LENGTH, len(text))
        )
    if not text.strip():
        raise ValueError("entry must not be only white space")
    return text


def write_entry(path, text):
    """Write text to path, then read it back and verify it byte-exactly.

    The read-back must have the same UTF-8 byte length as the entry
    (no trailing newline may sneak in), decode to the same text, and
    hash to the same sha256 digest.
    """
    validate_entry(text)
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    with open(path, "rb") as handle:
        raw = handle.read()
    intended = text.encode("utf-8")
    if len(raw) != len(intended) or raw != intended:
        raise ValueError("read-back mismatch: written bytes differ from entry")
    if hashlib.sha256(raw).hexdigest() != hashlib.sha256(intended).hexdigest():
        raise ValueError("read-back digest mismatch")
    return path


def output_path():
    """Entry destination: $MAKEFUN_OUTPUT_DIR/entry.txt, else /output."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out_dir:
        return os.path.join(out_dir, "entry.txt")
    return OUTPUT_PATH


def main():
    validate_entry(ENTRY)
    path = output_path()
    write_entry(path, ENTRY)
    print("wrote %d characters to %s" % (len(ENTRY), path))


if __name__ == "__main__":
    main()
