#!/usr/bin/env python3
"""Build the reviewed BAV-006 finite batch after human contextual reading."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
readings = json.loads((ROOT / "research/horse/bavli/BAV-006.read-excerpts.json").read_text())
covered = {
    "5b:29": "Already read and explicitly incorporated as continuation context in bavli-bekhorot-5b-28-davidson.",
    "6a:1": "Already read and explicitly incorporated as continuation context in bavli-bekhorot-5b-28-davidson.",
    "6a:3": "Already read and explicitly incorporated as continuation context in bavli-bekhorot-5b-28-davidson.",
    "6a:4": "Already read and explicitly incorporated as continuation context in bavli-bekhorot-5b-28-davidson.",
    "6a:5": "Already read and explicitly incorporated as continuation context in bavli-bekhorot-5b-28-davidson.",
}
analysis = {
    ("Bekhorot", "6a:13"): ("horse_like_offspring_hypothetical", "A donkey bearing horse-like young is posed as a legal classification problem for firstborn sanctity; this is morphological hypothetic reasoning, not evidence of miraculous cross-species reproduction."),
    ("Bekhorot", "6a:14"): ("horse_like_offspring_hypothetical", "A cow bearing horse-like young extends the legal classification problem across clean and unclean species; the passage tests the importance of bodily signs."),
    ("Bekhorot", "6a:15"): ("horse_like_offspring_hypothetical", "A baraita is tested against the case of cow or donkey producing horse-like young; the discussion concerns firstborn liability and partial identifying signs."),
    ("Bekhorot", "6a:16"): ("horse_like_offspring_hypothetical", "The baraita distinguishes horse-like appearance from partial maternal-species signs when determining firstborn liability."),
    ("Bekhorot", "6a:17"): ("horse_like_offspring_hypothetical", "The sugya explains why donkey bearing horse-like young is not redundant, comparing horns and split or unsplit hooves; it is legal morphology."),
    ("Bekhorot", "7a:23"): ("horse_urine_status", "Horse and camel urine are contrasted with cloudy donkey urine in a food-law inquiry; the stated rationale is that clear urine resembles ingested and excreted water."),
    ("Bekhorot", "7b:2"): ("horse_urine_status", "An alternative formulation excludes horse and camel urine from the practical question because people do not drink it; the live question concerns donkey urine used for jaundice."),
    ("Bekhorot", "40a:14"): ("horse_hoof_comparison", "A fused hoof like that of a donkey or horse defines the bodily defect קָלוּט in a firstborn-animal discussion."),
    ("Chagigah", "9b:12"): ("white_horse_proverb", "A proverb says poverty suits Jews like a red strap on a white horse; the horse supplies a visual comparison, not supernatural symbolism."),
    ("Chullin", "5a:1"): ("royal_horse_equivalence", "The verse 'my horses as your horses' is parsed as shared military fate, in an argument about Jehoshaphat’s association with Ahab; the horses are ordinary royal forces."),
    ("Chullin", "79a:2"): ("mule_parentage", "A dispute over paternal lineage classifies mule offspring by horse or donkey maternity and asks which pairings count as one kind."),
    ("Chullin", "79a:4"): ("mule_parentage", "The sugya identifies the Sages with Hananiah and treats horse-donkey and donkey-horse parentage as one mule kind under his view."),
    ("Chullin", "79a:7"): ("mule_parentage", "A proof attempt tests whether R. Judah disregards paternal seed by comparing offspring of mares sired by horses or donkeys."),
    ("Chullin", "79a:9"): ("mule_parentage", "The proof is rejected by reading both fathers as donkeys; 'horse side' and 'donkey side' describe mixed ancestry relevant to prohibited labor pairings."),
    ("Chullin", "79a:10"): ("mule_breeding_identification", "R. Judah forbids mating a female mule with either horse or donkey when its maternal kind is unknown; voice, ears and tail are proposed as lineage signs."),
}

sources, verdicts = [], []
for item in readings:
    c = item["candidate"]
    locator = c["locator"]
    if locator in covered:
        verdicts.append({**c, "task_id": "BAV-006", "verdict": "duplicate_context_covered", "reason": covered[locator], "registered_source_id": "bavli-bekhorot-5b-28-davidson"})
        continue
    role, interpretation = analysis[(c["work"], locator)]
    segment = locator.split(":", 1)[1]
    quote = item["read_segments"][segment]
    source_id = f"bavli-{c['work'].lower().replace(' ', '-')}-{locator.replace(':', '-')}-davidson"
    sources.append({
        "schema_version": 1, "id": source_id, "corpus_id": "bavli", "work": c["work"],
        "locator": locator, "url": f"https://www.sefaria.org/{c['work'].replace(' ', '_')}.{locator.replace(':', '.')}",
        "access_url": item["url"], "edition": item["edition"], "language": "Hebrew/Aramaic",
        "mention_type": "direct", "parent_source_id": None, "quote": quote,
        "context": f"Read the target and up to two adjacent segments on {c['work']} {locator}. {interpretation}",
        "checks": {"primary_read": True, "quote_verified": True, "context_checked": True, "attribution_verified": True, "commentaries_checked": False, "interpretation_prepared": True, "independent_reviewed": False},
        "interpretation": interpretation, "epistemic_type": "primary_text", "reviewers": ["coordinator-2026-10-11"],
        "task_id": "BAV-006", "role": role,
        "limitations": ["Digital API edition; no manuscript or printed-edition collation, traditional commentary review, or independent review.", "Legal and proverbial claims are retained as attributed discourse, not external historical or zoological verification."],
        "accessed_at": "2026-10-11"
    })
    verdicts.append({**c, "task_id": "BAV-006", "verdict": "accepted", "reason": interpretation, "source_id": source_id})

remaining = [json.loads(line) for line in (ROOT / "research/horse/bavli/BAV-005.remaining.jsonl").read_text().splitlines() if line.strip()][20:]
for row in remaining:
    row["task_id"] = "BAV-006"
    row["carried_from_task_id"] = "BAV-006"

def write_jsonl(path, rows):
    (ROOT / path).write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows))

write_jsonl("research/horse/bavli/BAV-006.sources.jsonl", sources)
write_jsonl("research/horse/bavli/BAV-006.verdicts.jsonl", verdicts)
write_jsonl("research/horse/bavli/BAV-006.remaining.jsonl", remaining)
report = f"""# BAV-006 — bounded primary context review

2026-10-11. Read the next 20 entries of the saved 43-candidate BAV-005 remainder in the named William Davidson digital witness, with up to two adjacent segments on each side.

- Accepted as separately registered direct contexts: **{len(sources)}**.
- Already covered by the explicit continuation note on `bavli-bekhorot-5b-28-davidson`: **{len(covered)}**. These were not double-counted.
- Remaining finite queue: **{len(remaining)}** candidates.

The batch is predominantly legal zoological classification: horse-like offspring in firstborn law, horse/camel urine, fused hooves, and horse–donkey ancestry of mules. Chagigah 9b:12 uses a white horse in a visual proverb; Chullin 5a:1 reads royal horses as shared military fate. **No entry in this batch describes a horse transporting a person between worlds, flying, or functioning as an independently established celestial species.** This negative statement is limited to these twenty candidate contexts.

Exact quotations and access URLs are in `BAV-006.sources.jsonl`; complete bounded reading receipts are in `BAV-006.read-excerpts.json`. No commentaries, manuscripts, printed witnesses, or independent reviews were added in this pass.
"""
(ROOT / "research/horse/bavli/BAV-006.report.md").write_text(report)
print(json.dumps({"accepted": len(sources), "covered": len(covered), "remaining": len(remaining)}))
