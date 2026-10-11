#!/usr/bin/env python3
"""Export a stable, human-readable subset of research/horse/data/sources.jsonl to CSV."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
INPUT = ROOT / 'research/horse/data' / "sources.jsonl"
OUTPUT = ROOT / 'research/horse/data' / "sources.csv"
FIELDS = [
    "id", "corpus_id", "work", "locator", "author", "language",
    "mention_type", "epistemic_type", "role", "categories", "quote",
    "context", "interpretation", "url", "edition", "task_id",
    "primary_read", "quote_verified", "context_checked",
    "attribution_verified", "commentaries_checked",
    "interpretation_prepared", "independent_reviewed", "reviewers",
    "limitations", "accessed_at",
]


def compact(value):
    if value is None:
        return ""
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return value


def main():
    records = [json.loads(line) for line in INPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        for source in records:
            checks = source.get("checks", {})
            row = {key: compact(source.get(key)) for key in FIELDS}
            for key in (
                "primary_read", "quote_verified", "context_checked",
                "attribution_verified", "commentaries_checked",
                "interpretation_prepared", "independent_reviewed",
            ):
                row[key] = checks.get(key, False)
            writer.writerow(row)
    print(f"wrote {len(records)} records to {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
