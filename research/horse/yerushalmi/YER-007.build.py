#!/usr/bin/env python3
"""Build the bounded YER-007 review from the saved YER-002 primary segments."""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "research/yerushalmi"

def lines(path):
    return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]

def write_lines(path, rows):
    path.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in rows))

remaining = lines(HERE / "YER-006.remaining.jsonl")
batch, tail = remaining[:15], remaining[15:]
candidates = {x["id"]: x for x in lines(HERE / "YER-002.candidates.jsonl")}
prior = lines(HERE / "YER-006.verdicts.jsonl")

accepted = {
    "yer-002-jerusalem-talmud-shabbat-6-1-3": {
        "mention_type": "indirect", "role": "horse_tail_hair_simile",
        "context": "Complete segment asks about tying strands and reports Rav Judah's practical ruling: a woman descending to immerse ties her hair like a horse's tail. Ordinary horse-tail simile; no supernatural movement."
    },
    "yer-002-jerusalem-talmud-shabbat-8-2-3": {
        "mention_type": "indirect", "role": "horse_tail_hair_material",
        "context": "Complete segment sets Sabbath carrying quantities for plant and animal materials. Two hairs from a horse's or cow's tail are liable because they are prepared for traps. Material-use rule, not a horse narrative."
    },
    "yer-002-jerusalem-talmud-shekalim-7-2-6": {
        "mention_type": "direct", "role": "horse_as_source_of_meat",
        "context": "Complete segment discusses the status of meat found in a non-Jew's possession. R. Eleazar b. Haggai sees a non-Jew cutting from his horse and taking it outside; the episode illustrates R. Johanan's rule and is qualified by R. Yose's report. Ordinary animal/meat context, not supernatural movement."
    },
}

reasons = {
    "yer-002-jerusalem-talmud-megillah-2-1-4": "Matched סוסרטי only within the personal name Samuel bar Susarti; not equine.",
    "yer-002-jerusalem-talmud-nazir-6-1-9": "Matches are the personal name Samuel bar Susarti and הריסוסין, crushed pieces; not equine.",
    "yer-002-jerusalem-talmud-nedarim-7-3-2": "סוסרנה is a goat-skin garment term in this clothing-vow discussion, not a horse reference.",
    "yer-002-jerusalem-talmud-rosh-hashanah-2-1-3": "סוסיתה is the place-name Susita/Hippos in an example about identifying witnesses; not equine.",
    "yer-002-jerusalem-talmud-rosh-hashanah-2-1-5": "סוסיתה is the place-name Susita/Hippos in a time-of-day report; not equine.",
    "yer-002-jerusalem-talmud-shabbat-7-2-24": "Substring match occurs in a non-equine technical phrase amid derivatives of gathering/threshing.",
    "yer-002-jerusalem-talmud-shabbat-8-3-1": "דוכסוסטוס is the parchment layer duxostos; substring only, not equine.",
    "yer-002-jerusalem-talmud-shabbat-8-3-3": "דוכסוסטון is the parchment layer duxostos; substring only, not equine.",
    "yer-002-jerusalem-talmud-sheviit-3-2-5": "גיפסוס means gypsum/plaster in a building-material list; substring only, not equine.",
    "yer-002-jerusalem-talmud-sheviit-6-1-13": "סוסיתא is the place-name Susita/Hippos, identified with the land of Tob; not equine.",
    "yer-002-jerusalem-talmud-sheviit-8-3-3": "סוסיתא is the place-name Susita/Hippos, source of imported produce; not equine.",
    "yer-002-jerusalem-talmud-shevuot-2-1-10": "Matched סוסרטי only within the personal name Simon bar Susarti; not equine.",
}

receipts, sources, fresh = [], [], []
for row in batch:
    c = candidates[row["candidate_id"]]
    receipts.append({
        "candidate_id": c["id"], "export_url": c["export_url"], "quote": c["quote"],
        "read_scope": "complete saved segment", "constituent_versions": c["constituent_versions"]
    })
    base = {"schema_version": 1, "candidate_id": c["id"], "task_id": "YER-007", "work": c["work"], "locator": c["locator"], "url": c["url"]}
    if c["id"] not in accepted:
        fresh.append({**base, "verdict": "rejected", "reason": reasons[c["id"]], "carried_from_task_id": "YER-006"})
        continue
    a = accepted[c["id"]]
    sid = c["id"].replace("yer-002-jerusalem-talmud-", "yerushalmi-") + "-guggenheimer"
    fresh.append({**base, "verdict": "accepted", "reason": a["context"], "registered_source_id": sid, "carried_from_task_id": "YER-006"})
    sources.append({
        "schema_version": 1, "id": sid, "corpus_id": "yerushalmi", "work": c["work"], "locator": c["locator"],
        "url": c["url"], "access_url": c["export_url"], "edition": c["constituent_versions"][0][0],
        "language": "Hebrew/Aramaic", "mention_type": a["mention_type"], "parent_source_id": None,
        "quote": c["quote"], "context": a["context"],
        "checks": {"primary_read": True, "quote_verified": True, "context_checked": True, "attribution_verified": True, "commentaries_checked": False, "interpretation_prepared": True, "independent_reviewed": False},
        "interpretation": a["context"], "epistemic_type": "primary_text", "reviewers": ["research-runner"],
        "task_id": "YER-007", "role": a["role"],
        "limitations": ["Complete saved YER-002 export-derived primary segment read; no fresh surrounding halakha retrieved.", "Merged export provenance not manuscript collation; no traditional commentaries or independent review."],
        "accessed_at": "2026-10-11"
    })

ledger = []
done_ids = {x["candidate_id"] for x in fresh}
for x in prior:
    ledger.append(next((y for y in fresh if y["candidate_id"] == x["candidate_id"]), x) if x["candidate_id"] in done_ids else x)

next_rows = [{**x, "task_id": "YER-007", "carried_from_task_id": "YER-006"} for x in tail]
write_lines(HERE / "YER-007.verdicts.jsonl", ledger)
write_lines(HERE / "YER-007.sources.jsonl", sources)
write_lines(HERE / "YER-007.remaining.jsonl", next_rows)
(HERE / "YER-007.read-excerpts.json").write_text(json.dumps(receipts, ensure_ascii=False, indent=2) + "\n")

counts = Counter(x["verdict"] for x in ledger)
report = f"""# YER-007 — bounded primary context review, 2026-10-11

15 previously pending candidates read: {len(sources)} accepted primary segment records ({sum(x['mention_type']=='direct' for x in sources)} direct, {sum(x['mention_type']=='indirect' for x in sources)} indirect); {15-len(sources)} rejected lexical false positives. Cumulative carried-forward discovery ledger: {dict(counts)}. Remaining: {len(next_rows)} candidates, unverified. This is not a full-corpus rescan or completeness claim.

"""
for s in sources:
    report += f"- {s['work']} {s['locator']}: {s['context']}\n"
report += "\nActual access URLs and exact Hebrew/Aramaic quotations are in sources; read-excerpts preserves named receipt scope. Yerushalmi review used the complete saved original export-derived segment, not all neighboring halakha. Commentary and independent-review flags remain false. No reliable ancient dating or historical verification is inferred from modern edition metadata.\n"
(HERE / "YER-007.report.md").write_text(report)
