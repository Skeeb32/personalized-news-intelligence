"""Validate punctuation, not factual accuracy or permission to publish."""
import argparse
from pathlib import Path
import sys
import unicodedata


def issues(text):
    if not text.strip():
        yield "Post is empty."
    for row, line in enumerate(text.splitlines(), 1):
        for col, char in enumerate(line, 1):
            if unicodedata.category(char) == "Pd" or char in "\u00ad\u2212":
                yield f"Line {row}, column {col}: forbidden {unicodedata.name(char, 'dash')} (U+{ord(char):04X})."


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("post", type=Path)
    args = parser.parse_args()
    try:
        errors = list(issues(args.post.read_text(encoding="utf-8")))
    except (OSError, UnicodeError) as exc:
        print(f"Cannot read post: {exc}", file=sys.stderr)
        return 1
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("Formatting passed. Facts, sources, originality and authorization still require review.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
