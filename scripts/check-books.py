#!/usr/bin/env python3
"""Checks for the book pipeline. Standard library only.

Syntax-checks every script in books/scripts and sanity-checks the prompt manifest:
required columns present, no blank titles or objects, page numbers are integers, and
each book has no duplicate page numbers. Run from the repository root.
"""
import csv
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = {"book_slug", "book_title", "page", "object_name", "prompt", "fact", "status", "asset_path"}


def main() -> int:
    errors = []
    scripts = sorted((ROOT / "books" / "scripts").glob("*.py"))
    for script in scripts:
        try:
            compile(script.read_text(encoding="utf-8"), str(script), "exec")
        except SyntaxError as exc:
            errors.append(f"{script.relative_to(ROOT)}:{exc.lineno}: {exc.msg}")
    manifest = ROOT / "books" / "prompts" / "manifest-v2.csv"
    rows = 0
    if not manifest.exists():
        errors.append("books/prompts/manifest-v2.csv is missing")
    else:
        with manifest.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            missing = REQUIRED - set(reader.fieldnames or [])
            if missing:
                errors.append(f"manifest-v2.csv: missing columns {sorted(missing)}")
            else:
                seen = defaultdict(set)
                for line, row in enumerate(reader, start=2):
                    rows += 1
                    if not row["book_title"].strip() or not row["object_name"].strip():
                        errors.append(f"manifest-v2.csv line {line}: blank title or object")
                    try:
                        page = int(row["page"])
                    except ValueError:
                        errors.append(f"manifest-v2.csv line {line}: page {row['page']!r} is not an integer")
                        continue
                    if page in seen[row["book_slug"]]:
                        errors.append(f"manifest-v2.csv line {line}: duplicate page {page} in {row['book_slug']}")
                    seen[row["book_slug"]].add(page)
    for line in errors:
        print(f"ERROR {line}")
    print(f"compiled {len(scripts)} scripts, checked {rows} manifest rows, {len(errors)} problem(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
