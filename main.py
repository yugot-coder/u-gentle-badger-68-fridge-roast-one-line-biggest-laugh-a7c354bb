"""Fridge Roast: One Line, Biggest Laugh.

Writes a single roast line for a smart fridge to /output/entry.txt.

Standard library only. Deterministic: the same entry text is written
on every run.
"""

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
    """Write text to path, then read it back and verify it matches."""
    validate_entry(text)
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    with open(path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != text:
        raise ValueError("read-back mismatch: written text differs from entry")
    return path


def main():
    validate_entry(ENTRY)
    write_entry(OUTPUT_PATH, ENTRY)
    print("wrote %d characters to %s" % (len(ENTRY), OUTPUT_PATH))


if __name__ == "__main__":
    main()
