#!/usr/bin/env python3
"""Reconcile the 2026-10-11 checkpoint from committed task artifacts."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def load_jsonl(path):
    return [json.loads(line) for line in (ROOT / path).read_text().splitlines() if line.strip()]


def save_jsonl(path, rows):
    (ROOT / path).write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows))


def main():
    tasks = load_jsonl("research/horse/state/tasks.jsonl")
    updates = {
        "BAV-005": ("done", [
            "research/horse/bavli/BAV-005.read-excerpts.json", "research/horse/bavli/BAV-005.verdicts.jsonl",
            "research/horse/bavli/BAV-005.remaining.jsonl", "research/horse/bavli/BAV-005.sources.jsonl",
            "research/horse/bavli/BAV-005.report.md"]),
        "YER-006": ("done", [
            "research/horse/yerushalmi/YER-006.read-excerpts.json", "research/horse/yerushalmi/YER-006.verdicts.jsonl",
            "research/horse/yerushalmi/YER-006.remaining.jsonl", "research/horse/yerushalmi/YER-006.sources.jsonl",
            "research/horse/yerushalmi/YER-006.report.md"]),
        "COM-004": ("partial", [
            "research/horse/commentaries/COM-004.coverage.json", "research/horse/commentaries/COM-004.discoveries.jsonl",
            "research/horse/commentaries/COM-004.manifest.json", "research/horse/commentaries/COM-004.fetch.py"]),
        "VER-007": ("done", [
            "research/horse/verification/VER-007.contexts.json", "research/horse/verification/VER-007.biblical-contexts.json",
            "research/horse/verification/VER-007.reviews.jsonl", "research/horse/verification/VER-007.report.md"]),
        "TAN-AUDIT": ("done", [
            "research/horse/tanakh/TAN-AUDIT.build.py", "research/horse/tanakh/TAN-AUDIT.report.md",
            "reports/horse/tanakh-catalogue.md"]),
        "CHR-002": ("partial", [
            "research/horse/provenance/CHR001.evidence.jsonl", "research/horse/provenance/CHR001.chronology.jsonl",
            "research/horse/provenance/CHR001.report.md"]),
        "VER-007p": ("done", [
            "research/horse/verification/VER-007p.review.jsonl", "research/horse/verification/VER-007p.report.md"]),
    }
    for task in tasks:
        if task["id"] in updates:
            task["status"], task["results"] = updates[task["id"]]
            task["assignment"] = None
            task["updated_at"] = "2026-10-11"
    existing = {task["id"] for task in tasks}
    additions = [
        ("BAV-006", "Review the next 20 of 43 remaining Bavli candidates", "BAV-005"),
        ("YER-007", "Review the next 15 of 24 remaining Yerushalmi candidates", "YER-006"),
    ]
    for task_id, goal, dependency in additions:
        if task_id not in existing:
            tasks.append({
                "id": task_id, "goal": goal, "corpus": "bounded follow-up",
                "queries": ["saved finite remaining ledger"], "depends_on": [dependency],
                "expected_output": "task-specific JSONL and report with exact bounded scope",
                "completion_criteria": "Named finite batch read in primary context; verdicts, sources, remainder and limits saved",
                "status": "pending", "results": [],
                "limitations": ["Completion applies only to the named batch; corpus completeness remains qualified."],
                "open_questions": [], "assignment": None, "updated_at": "2026-10-11"
            })
    save_jsonl("research/horse/state/tasks.jsonl", tasks)

    sources = load_jsonl("research/horse/data/sources.jsonl")
    stats = {
        "records": len(sources),
        "context_checked": sum(bool(s["checks"]["context_checked"]) for s in sources),
        "independently_reviewed": sum(bool(s["checks"]["independent_reviewed"]) for s in sources),
    }
    project_path = ROOT / "research/horse/state/project.json"
    project = json.loads(project_path.read_text())
    project["session_id"] = "research-2026-10-11-01"
    project["active_task_ids"] = []
    project["pending_task_ids"] = ["BAV-006", "YER-007", "COM-004", "CHR-001", "CHR-002", "KAB-002", "SYN-001", "CMP-001", "AUD-001"]
    project["next_action"] = "Run BAV-006 and YER-007 from the saved finite ledgers; finish COM-004 normalization and CHR-002 bibliography; then synthesis/comparison/audit."
    project["active_workers"] = []
    project["registry_statistics"] = stats
    project_path.write_text(json.dumps(project, ensure_ascii=False, indent=2) + "\n")

    coverage_path = ROOT / "research/horse/data/coverage.json"
    coverage = json.loads(coverage_path.read_text())
    coverage["registry_statistics"] = stats
    coverage["checkpoint_note"] = "Recovered artifact truth on 2026-10-11: TAN-AUDIT, BAV-005, YER-006, VER-007 and VER-007p completed as bounded tasks; BAV 43 and YER 24 candidates remain; COM-004 and chronology remain partial."
    coverage_path.write_text(json.dumps(coverage, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
