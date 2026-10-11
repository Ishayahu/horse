#!/usr/bin/env python3
import json
from pathlib import Path
R=Path(__file__).resolve().parents[3]
def rows(p): return [json.loads(x) for x in (R/p).read_text().splitlines() if x.strip()]
def save(p,x): (R/p).write_text(''.join(json.dumps(y,ensure_ascii=False)+'\n' for y in x))
t=rows('research/horse/state/tasks.jsonl')
for x in t:
 if x['id']=='KAB-002':
  x['status']='done'; x['results']=['research/horse/kabbalah/KAB-002.read.py','research/horse/kabbalah/KAB-002.access.json','research/horse/kabbalah/KAB-002.sources.jsonl','research/horse/kabbalah/KAB-002.report.md']; x['limitations']=['Named seven-passage Ari-school batch complete; recension/manuscript coverage and exact redaction history remain unresolved.']; x['updated_at']='2026-10-11'
save('research/horse/state/tasks.jsonl',t)
p=R/'research/horse/state/project.json'; q=json.loads(p.read_text()); q['pending_task_ids']=[x for x in q['pending_task_ids'] if x!='KAB-002']; q['next_action']='Produce SYN-001 qualified thematic synthesis, then CMP-001 comparison and AUD-001 final audit.'; q['last_confirmed_commit']='33e0cdaa3378c7732e375ba8e5ba2b9ed7dc3666'; p.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
p=R/'research/horse/data/coverage.json'; c=json.loads(p.read_text()); c['checkpoint_note']='KAB-002 closed from seven existing verified contextual records; Lurianic horse imagery is symbolic/moral and does not establish Pegasus or literal interworld horse transport. Synthesis is next.'; p.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
p=R/'research/horse/state/handoff.md'; z=p.read_text().replace('Последний подтверждённый предшествующий коммит: 4f9f51b12491ce978bf495b4641bf0d9d9a66b7b.','Последний подтверждённый предшествующий коммит: 33e0cdaa3378c7732e375ba8e5ba2b9ed7dc3666.').replace('Продолжать со сверки KAB-002, затем переходить к синтезу, сравнению и аудиту.','KAB-002 завершён по семи сохранённым контекстам школы Аризаля. Продолжать с SYN-001, затем CMP-001 и AUD-001.')
p.write_text(z)
