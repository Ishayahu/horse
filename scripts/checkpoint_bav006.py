#!/usr/bin/env python3
"""Publish the bounded BAV-006 state transition after artifact validation."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load_lines(path):
    return [json.loads(line) for line in (ROOT / path).read_text().splitlines() if line.strip()]

def save_lines(path, rows):
    (ROOT / path).write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows))

tasks = load_lines("state/tasks.jsonl")
for task in tasks:
    if task["id"] == "BAV-006":
        task["status"] = "done"
        task["results"] = [
            "research/bavli/BAV-006.fetch.py", "research/bavli/BAV-006.build.py",
            "research/bavli/BAV-006.read-excerpts.json", "research/bavli/BAV-006.verdicts.jsonl",
            "research/bavli/BAV-006.sources.jsonl", "research/bavli/BAV-006.remaining.jsonl",
            "research/bavli/BAV-006.report.md"
        ]
        task["updated_at"] = "2026-10-11"
if not any(task["id"] == "BAV-007" for task in tasks):
    tasks.append({
        "id": "BAV-007", "goal": "Review the final 23 Bavli candidates", "corpus": "bounded follow-up",
        "queries": ["research/bavli/BAV-006.remaining.jsonl"], "depends_on": ["BAV-006"],
        "expected_output": "Final finite-ledger verdicts, sources, zero-or-qualified remainder and report",
        "completion_criteria": "All 23 named candidates read in primary context and finite remainder resolved",
        "status": "pending", "results": [],
        "limitations": ["Finite discovery-ledger completion will not establish absolute completeness of every spelling, edition, commentary or manuscript."],
        "open_questions": [], "assignment": None, "updated_at": "2026-10-11"
    })
save_lines("state/tasks.jsonl", tasks)

sources = load_lines("data/sources.jsonl")
stats = {"records": len(sources), "context_checked": sum(bool(s["checks"]["context_checked"]) for s in sources), "independently_reviewed": sum(bool(s["checks"]["independent_reviewed"]) for s in sources)}
project_path = ROOT / "state/project.json"
project = json.loads(project_path.read_text())
project["pending_task_ids"] = ["BAV-007" if task == "BAV-006" else task for task in project["pending_task_ids"]]
project["next_action"] = "Run YER-007 or final Bavli batch BAV-007; then finish COM-004 normalization and chronology before synthesis/comparison/audit."
project["registry_statistics"] = stats
project_path.write_text(json.dumps(project, ensure_ascii=False, indent=2) + "\n")

coverage_path = ROOT / "data/coverage.json"
coverage = json.loads(coverage_path.read_text())
for corpus in coverage["corpora"]:
    if corpus["id"] == "bavli":
        corpus["confirmed_count"] += 15
        corpus["limitations"] = ["Finite lexical discovery ledger has 23 candidates still pending after BAV-006; counts are contextual records, not proof of absolute corpus completeness."]
        corpus["next_checks"] = ["BAV-007 final 23-candidate review", "Independent review of central extraordinary/spiritual passages"]
coverage["registry_statistics"] = stats
coverage["checkpoint_note"] = "BAV-006 read 20 named remaining candidates: 15 registered contexts, 5 already covered continuations, 23 finite-ledger candidates remain; YER 24 remain; COM-004 and chronology remain partial."
coverage_path.write_text(json.dumps(coverage, ensure_ascii=False, indent=2) + "\n")

handoff = ROOT / "state/handoff.md"
text = handoff.read_text()
text = text.replace("465 записей, 463 с проверенным контекстом", "480 записей, 478 с проверенным контекстом")
text = text.replace("В конечных очередях остаются BAV 43 и YER 24 кандидата; следующие партии — BAV-006 и YER-007.", "BAV-006 завершён: из 20 кандидатов 15 зарегистрированы отдельно, 5 оказались уже прочитанными продолжениями; в конечной очереди Бавли осталось 23 кандидата (`BAV-007`). В Иерушалми остаются 24 кандидата (`YER-007` — следующая партия 15).")
text = text.replace("Продолжать с BAV-006/YER-007", "Продолжать с YER-007 или финальным BAV-007")
handoff.write_text(text)
