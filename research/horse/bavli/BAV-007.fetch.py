#!/usr/bin/env python3
"""Fetch final BAV-007 candidate batch and bounded adjacent context from Sefaria."""
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
rows = [json.loads(line) for line in (ROOT / "research/horse/bavli/BAV-006.remaining.jsonl").read_text().splitlines() if line.strip()]
pages, out = {}, []
for row in rows:
    daf, segment = row["locator"].split(":")
    key = (row["work"], daf)
    if key not in pages:
        ref = urllib.parse.quote(f'{row["work"]}.{daf}')
        url = f"https://www.sefaria.org/api/texts/{ref}?context=0&commentary=0"
        with urllib.request.urlopen(url, timeout=60) as response:
            pages[key] = json.load(response)
        time.sleep(0.2)
    page = pages[key]
    index = int(segment) - 1
    lo, hi = max(0, index - 2), min(len(page["he"]), index + 3)
    out.append({
        "candidate": {**row, "task_id": "BAV-007"},
        "url": f"https://www.sefaria.org/api/texts/{urllib.parse.quote(row['work'] + '.' + daf)}?context=0&commentary=0",
        "edition": page.get("heVersionTitle"), "license": page.get("heLicense"),
        "read_segments": {str(i + 1): re.sub(r"<[^>]+>", "", page["he"][i]) for i in range(lo, hi)},
    })
(ROOT / "research/horse/bavli/BAV-007.read-excerpts.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"saved": len(out), "dapim": len(pages)}))
