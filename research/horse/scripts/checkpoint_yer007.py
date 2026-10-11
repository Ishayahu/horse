#!/usr/bin/env python3
"""Publish the bounded YER-007 state transition after artifact validation."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def load_lines(path):
    return [json.loads(x) for x in (ROOT / path).read_text().splitlines() if x.strip()]
def save_lines(path, rows):
    (ROOT / path).write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in rows))

tasks = load_lines("state/tasks.jsonl")
for task in tasks:
    if task["id"] == "YER-007":
        task["status"] = "done"
        task["results"] = [
            "research/yerushalmi/YER-007.build.py", "research/yerushalmi/YER-007.read-excerpts.json",
            "research/yerushalmi/YER-007.verdicts.jsonl", "research/yerushalmi/YER-007.sources.jsonl",
            "research/yerushalmi/YER-007.remaining.jsonl", "research/yerushalmi/YER-007.report.md"
        ]
        task["updated_at"] = "2026-10-11"
if not any(x["id"] == "YER-008" for x in tasks):
    tasks.append({
        "id": "YER-008", "goal": "Review the final 9 Yerushalmi candidates", "corpus": "bounded follow-up",
        "queries": ["research/yerushalmi/YER-007.remaining.jsonl"], "depends_on": ["YER-007"],
        "expected_output": "Final finite-ledger verdicts, sources, zero-or-qualified remainder and report",
        "completion_criteria": "All 9 named candidates read in primary context and finite remainder resolved",
        "status": "pending", "results": [],
        "limitations": ["Finite discovery-ledger completion will not establish absolute completeness of every spelling, edition, commentary or manuscript."],
        "open_questions": [], "assignment": None, "updated_at": "2026-10-11"
    })
save_lines("state/tasks.jsonl", tasks)

sources = load_lines("data/sources.jsonl")
stats = {"records": len(sources), "context_checked": sum(x["checks"]["context_checked"] for x in sources), "independently_reviewed": sum(x["checks"]["independent_reviewed"] for x in sources)}
project_path = ROOT / "state/project.json"
project = json.loads(project_path.read_text())
project["pending_task_ids"] = ["YER-008" if x == "YER-007" else x for x in project["pending_task_ids"]]
project["next_action"] = "Run final Yerushalmi batch YER-008 or final Bavli batch BAV-007; then finish COM-004 normalization and chronology before synthesis/comparison/audit."
project["last_confirmed_commit"] = "16cec116b0ffed9d26535d860bd8f3139940f95c"
project["registry_statistics"] = stats
project_path.write_text(json.dumps(project, ensure_ascii=False, indent=2) + "\n")

coverage_path = ROOT / "data/coverage.json"
coverage = json.loads(coverage_path.read_text())
for corpus in coverage["corpora"]:
    if corpus["id"] == "yerushalmi":
        corpus["confirmed_count"] += 3
        corpus["limitations"] = ["Finite lexical discovery ledger has 9 candidates still pending after YER-007; counts are contextual records, not proof of absolute corpus completeness.", "Niddah mixed provenance/license and rare Makkot witness identification remain unresolved."]
        corpus["next_checks"] = ["YER-008 final 9-candidate review", "Independent review of central extraordinary/spiritual passages"]
coverage["registry_statistics"] = stats
coverage["checkpoint_note"] = "YER-007 read 15 named remaining candidates: 3 registered contexts, 12 lexical false positives, 9 finite-ledger candidates remain; BAV 23 remain; COM-004 and chronology remain partial."
coverage_path.write_text(json.dumps(coverage, ensure_ascii=False, indent=2) + "\n")

handoff = ROOT / "state/handoff.md"
text = handoff.read_text()
text = text.replace("Последний подтверждённый предшествующий коммит: 284fafe7b2606c9b0501d15020f337f96d332284.", "Последний подтверждённый предшествующий коммит: 16cec116b0ffed9d26535d860bd8f3139940f95c.")
text = text.replace("480 записей, 478 с проверенным контекстом", "483 записи, 481 с проверенным контекстом")
text = text.replace("YER-006 (ограниченная партия 15)", "YER-006 и YER-007 (ограниченные партии по 15)")
text = text.replace("В Иерушалми остаются 24 кандидата (`YER-007` — следующая партия 15).", "YER-007 завершён: 3 контекста приняты, 12 лексических ложных совпадений отклонены; в конечной очереди Иерушалми осталось 9 кандидатов (`YER-008`).")
text = text.replace("Продолжать с YER-007 или финальным BAV-007", "Продолжать с финальным YER-008 или финальным BAV-007")
handoff.write_text(text)
