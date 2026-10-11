#!/usr/bin/env python3
import json
from pathlib import Path
R=Path(__file__).resolve().parents[3]
def rows(p): return [json.loads(x) for x in (R/p).read_text().splitlines() if x.strip()]
def save(p,x): (R/p).write_text(''.join(json.dumps(y,ensure_ascii=False)+'\n' for y in x))
t=rows('research/horse/state/tasks.jsonl')
for x in t:
 if x['id']=='CHR-001':
  x['status']='done'; x['results']=['research/horse/provenance/CHR001.evidence.jsonl','research/horse/provenance/CHR001.chronology.jsonl','research/horse/provenance/CHR001.report.md']; x['limitations']=['No selected horse passage has an earliest manuscript witness established; work-level dates remain separate.']; x['updated_at']='2026-10-11'
 if x['id']=='CHR-002':
  x['status']='done'; x['results']=['research/horse/provenance/CHR001.evidence.jsonl','research/horse/provenance/CHR001.chronology.jsonl','research/horse/provenance/CHR001.report.md','research/horse/provenance/CHR002.report.md']; x['limitations']=['Bounded bibliographic audit completed with passage-level earliest witnesses honestly unresolved.']; x['updated_at']='2026-10-11'
save('research/horse/state/tasks.jsonl',t)
p=R/'research/horse/state/project.json'; q=json.loads(p.read_text()); q['pending_task_ids']=[x for x in q['pending_task_ids'] if x not in {'CHR-001','CHR-002'}]; q['next_action']='Resolve KAB-002 artifact status, then synthesis/comparison/audit.'; q['last_confirmed_commit']='4f9f51b12491ce978bf495b4641bf0d9d9a66b7b'; p.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
p=R/'research/horse/data/coverage.json'; c=json.loads(p.read_text()); c['checkpoint_note']='CHR-001/CHR-002 bounded chronology audit closed with passage-level earliest witnesses explicitly unresolved; these limits constrain borrowing/priority claims but do not block qualified synthesis.'; p.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
p=R/'research/horse/state/handoff.md'; z=p.read_text().replace('Последний подтверждённый предшествующий коммит: b0f1b2d39f21a7fe24131d96ac01de5a69afc192.','Последний подтверждённый предшествующий коммит: 4f9f51b12491ce978bf495b4641bf0d9d9a66b7b.').replace('CHR-001/CHR-002 остаются partial.','CHR-001/CHR-002 завершены как ограниченный библиографический аудит; ранние свидетели конкретных конных пассажей в большинстве случаев честно оставлены неизвестными.').replace('Продолжать с хронологии CHR-001/CHR-002, затем сверить KAB-002 перед синтезом.','Продолжать со сверки KAB-002, затем переходить к синтезу, сравнению и аудиту.')
p.write_text(z)
