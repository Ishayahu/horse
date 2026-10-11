#!/usr/bin/env python3
"""Validate HORSE checkpoint; no network/dependencies required."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
def read(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))
def rows(path):
    return [json.loads(s) for s in (ROOT/path).read_text(encoding="utf-8").splitlines() if s.strip()]
def require(ok, message):
    if not ok: raise ValueError(message)
def validate():
    project, coverage = read("research/horse/state/project.json"), read("research/horse/data/coverage.json")
    require(project["schema_version"] == coverage["schema_version"] == 1, "Unsupported schema")
    tasks = rows("research/horse/state/tasks.jsonl")
    sources = rows("research/horse/data/sources.jsonl")
    refs = rows("research/horse/data/references.jsonl")
    hypotheses = rows("research/horse/data/hypotheses.jsonl")
    decisions = rows("research/horse/state/decisions.jsonl")
    for name, records in [("tasks",tasks),("sources",sources),("references",refs),("hypotheses",hypotheses),("decisions",decisions)]:
        ids=[r["id"] for r in records]
        require(len(ids)==len(set(ids)), "Duplicate IDs: "+name)
    by_id={t["id"]:t for t in tasks}
    visited, visiting=set(),set()
    def visit(tid):
        require(tid in by_id,"Missing dependency: "+tid)
        require(tid not in visiting,"Dependency cycle: "+tid)
        if tid in visited: return
        visiting.add(tid)
        for dep in by_id[tid]["depends_on"]: visit(dep)
        visiting.remove(tid); visited.add(tid)
    fields={"id","goal","corpus","queries","depends_on","expected_output","completion_criteria","status","results","limitations","open_questions","assignment","updated_at"}
    for t in tasks:
        require(fields <= set(t), "Incomplete task: "+t["id"])
        require(t["status"] in {"pending","running","partial","blocked","done"},"Invalid status")
        visit(t["id"])
        for path in t["results"]:
            require((ROOT/path).is_file(),"Missing result: "+path)
        if t["status"]=="done": require(bool(t["results"]),"Done task has no result")
    for key in ("active_task_ids","pending_task_ids"):
        require(set(project[key]) <= set(by_id), "Unknown project task")
    require(set(project["active_task_ids"]) == {t["id"] for t in tasks if t["status"]=="running"}, "Active queue mismatch")
    require(set(project["pending_task_ids"]) == {t["id"] for t in tasks if t["status"] in {"pending","partial"}}, "Pending queue mismatch")
    corpora=coverage["corpora"]
    require(len({c["id"] for c in corpora})==len(corpora),"Duplicate corpora")
    for c in corpora:
        require(c["status"] in {"not_started","partial","processed","unavailable"},"Invalid coverage status")
        for key in ("candidate_count","confirmed_count","commentary_count"):
            require(isinstance(c[key],int) and c[key]>=0,"Invalid counter")
        require(c["confirmed_count"]<=c["candidate_count"],"Confirmed exceeds candidates")
    sids={s["id"] for s in sources}
    check_keys={"primary_read","quote_verified","context_checked","attribution_verified","commentaries_checked","interpretation_prepared","independent_reviewed"}
    for s in sources:
        require(s["task_id"] in by_id,"Unknown source task")
        require(s["mention_type"] in {"direct","indirect"},"Invalid mention type")
        require(check_keys <= set(s["checks"]),"Missing checks")
        require(all(type(v) is bool for v in s["checks"].values()),"Checks must be boolean")
        if s["checks"]["quote_verified"]: require(bool(s["quote"]) and bool(s["url"]),"Verified quote lacks evidence")
        if s["checks"]["independent_reviewed"]: require(len(set(s["reviewers"]))>=2,"Independent review lacks two reviewers")
        if s.get("parent_source_id"): require(s["parent_source_id"] in sids,"Missing parent source")
    for r in refs:
        require(r["source_id"] in sids and r["target_source_id"] in sids,"Dangling reference")
    for h in hypotheses:
        require(set(h["source_ids"])<=sids,"Unknown hypothesis source")
        require(set(h["followup_task_ids"])<=set(by_id),"Unknown hypothesis task")
    sha=project["last_confirmed_commit"]
    require(isinstance(sha,str) and len(sha)==40 and all(c in "0123456789abcdef" for c in sha),"Invalid previous commit")
    require((ROOT/"research/horse/state/handoff.md").is_file(),"Missing handoff")
    print("HORSE state valid")
if __name__=="__main__": validate()
